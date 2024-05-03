# chainstate-cli
Interact with the Polkadot/Kusama blockchain via SubstrateInterface

## CLI

| Argument            | Default                        | Requires Value     |
|---------------------|--------------------------------|--------------------|
| --url               | wss://rpc.ibp.network/polkadot | :x:                | 
| --ref_caller        | None                           | :heavy_check_mark: |


#### --ref_caller [ongoing-ref-index]
> .\chainstate.py --url wss://rpc.ibp.network/polkadot --ref_caller 707
```json
{
    "call_index": "0x1305",
    "call_function": "spend",
    "call_module": "Treasury",
    "call_args": [
        {
            "name": "asset_kind",
            "type": "AssetKind",
            "value": {
                "V3": {
                    "location": {
                        "parents": 0,
                        "interior": {
                            "X1": {
                                "Parachain": 1000
                            }
                        }
                    },
                    "asset_id": {
                        "Concrete": {
                            "parents": 0,
                            "interior": {
                                "X2": [
                                    {
                                        "PalletInstance": 50
                                    },
                                    {
                                        "GeneralIndex": 19840000000000
                                    }
                                ]
                            }
                        }
                    }
                }
            }
        },
        {
            "name": "amount",
            "type": "AssetBalanceOf<T, I>",
            "value": 690000000000000000
        },
        {
            "name": "beneficiary",
            "type": "BeneficiaryLookupOf<T, I>",
            "value": {
                "V3": {
                    "parents": 0,
                    "interior": {
                        "X1": {
                            "AccountId32": {
                                "network": null,
                                "id": "0x2f944a1d1c5688dd06bc0335fb0bb058fa7fb2805a4247047dbbbc6c15121bc9"
                            }
                        }
                    }
                }
            }
        },
        {
            "name": "valid_from",
            "type": "Option<BlockNumberFor>",
            "value": null
        }
    ],
    "call_hash": "0x298451f2ff61458d669389eda0e3f3208fa2718df536e87496d8068adf759f61"
}
```
