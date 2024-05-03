from substrateinterface import SubstrateInterface
from websocket._exceptions import WebSocketException
from scalecodec.base import ScaleBytes
import argparse
import json


class MaterializedChainState:
    def __init__(self, url="wss://rpc.ibp.network/polkadot"):
        try:
            self.substrate = SubstrateInterface(url=url, auto_reconnect=True, ws_options={'close_timeout': 15, 'open_timeout': 15})
        except WebSocketException as error:
            print(f"Unable to connect: {error.args}")
            exit()

    def ref_caller(self, index: int):
        try:
            referendum = self.substrate.query(module='Referenda', storage_function='ReferendumInfoFor', params=[index]).serialize()
            if referendum is None or 'Ongoing' not in referendum:
                return False, f"Referendum #{index} not active"

            preimage = referendum['Ongoing']['proposal']

            if 'Inline' in preimage:
                call = preimage['Inline']
                call_obj = self.substrate.create_scale_object('Call')
                decoded_call = call_obj.decode(ScaleBytes(call))
                return json.dumps(decoded_call, indent=4)

            if 'Lookup' in preimage:
                preimage_hash = preimage['Lookup']['hash']
                preimage_length = preimage['Lookup']['len']

                call = self.substrate.query(module='Preimage', storage_function='PreimageFor', params=[(preimage_hash, preimage_length)]).value
                call_obj = self.substrate.create_scale_object('Call')
                decoded_call = call_obj.decode(ScaleBytes(call))
                return json.dumps(decoded_call, indent=4)
        except Exception as ref_caller_error:
            raise ref_caller_error


def main():
    parser = argparse.ArgumentParser(description='Interact with the Polkadot/Substrate blockchain via SubstrateInterface')
    parser.add_argument('--url', default="wss://rpc.ibp.network/polkadot", help='Specify the URL of the blockchain (default: wss://rpc.ibp.network/polkadot)')
    parser.add_argument('--ref_caller', type=int, help='Index of the referendum')
    args = parser.parse_args()
    chain_state = MaterializedChainState(url=args.url)

    if args.ref_caller:
        result = chain_state.ref_caller(args.ref_caller)
        print(result)


if __name__ == '__main__':
    main()
