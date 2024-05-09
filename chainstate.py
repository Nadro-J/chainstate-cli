from substrateinterface import SubstrateInterface
from websocket._exceptions import WebSocketException
from scalecodec.base import ScaleBytes
import argparse
import json


class MaterializedChainState:
    def __init__(self, url="wss://rpc.ibp.network/polkadot"):
        try:
            self.substrate = SubstrateInterface(url=url,
                                                auto_reconnect=True,
                                                ws_options={'close_timeout': 15, 'open_timeout': 15})
        except WebSocketException as error:
            print(f"Unable to connect: {error.args}")
            exit()

    def ref_caller(self, index: int, gov1: bool, call_data: bool):
        try:
            referendum = self.substrate.query(module="Democracy" if gov1 else "Referenda",
                                              storage_function="ReferendumInfoOf" if gov1 else "ReferendumInfoFor",
                                              params=[index]).serialize()

            if referendum is None or 'Ongoing' not in referendum:
                return False, f"Referendum #{index} not active"

            preimage = referendum['Ongoing']['proposal']

            if 'Inline' in preimage:
                call = preimage['Inline']
                if not call_data:
                    call_obj = self.substrate.create_scale_object('Call')
                    decoded_call = call_obj.decode(ScaleBytes(call))
                    return json.dumps(decoded_call, indent=4)
                else:
                    return call

            if 'Lookup' in preimage:
                preimage_hash = preimage['Lookup']['hash']
                preimage_length = preimage['Lookup']['len']
                call = self.substrate.query(module='Preimage', storage_function='PreimageFor', params=[(preimage_hash, preimage_length)]).value

                if not call.isprintable():
                    call = f"0x{''.join(f'{ord(c):02x}' for c in call)}"

                if not call_data:
                    call_obj = self.substrate.create_scale_object('Call')
                    decoded_call = call_obj.decode(ScaleBytes(call))
                    return json.dumps(decoded_call, indent=4)
                else:
                    return call
        except Exception as ref_caller_error:
            raise ref_caller_error

    def all_proxies(self):
        data = {}
        proxies = self.substrate.query_map(module='Proxy', storage_function='Proxies', params=[])
        for proxied_account, proxies in proxies:
            data.update({proxied_account.value: proxies[0].value})

        return json.dumps(data, indent=4)


def main():
    parser = argparse.ArgumentParser(description='Interact with the Polkadot/Substrate blockchain via SubstrateInterface')
    parser.add_argument('--url', default="wss://rpc.ibp.network/polkadot", help='Specify the URL of the blockchain (default: wss://rpc.ibp.network/polkadot)')
    parser.add_argument('--ref_caller', type=int, help='Index of the referendum')
    parser.add_argument('--gov1', action='store_true', default=False, help='Flag to indicate whether --gov1 is specified')
    parser.add_argument('--proxies', action='store_true', default=False, help='List all proxy accounts')
    parser.add_argument('--call_data', action='store_true', default=False, help='Get the Call Data hash of an ongoing proposal')
    parser.add_argument('--output', '-o', type=str, help='Output file path')
    args = parser.parse_args()
    chain_state = MaterializedChainState(url=args.url)
    if args.ref_caller:
        result = chain_state.ref_caller(args.ref_caller, args.gov1, args.call_data)
        print(result)

        if args.output:
            with open(f"./data/{args.output}", 'w') as f:
                f.write(result)
                print(f"Data has been written to ./data/{args.output}")

    if args.proxies:
        result = chain_state.all_proxies()
        print(result)

        if args.output:
            with open(f"./data/{args.output}", 'w') as f:
                f.write(result)
                print(f"Data has been written to./data/{args.output}")


if __name__ == '__main__':
    main()
