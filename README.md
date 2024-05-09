# chainstate-cli
Interact with the Polkadot/Kusama blockchain via SubstrateInterface

## CLI

| Argument     | Default                        | Requires Value     | Description           |
|--------------|--------------------------------|--------------------|-----------------------|
| --url        | wss://rpc.ibp.network/polkadot | :x:                | RPC url               | 
| --ref_caller | None                           | :heavy_check_mark: | Referendum Index      |
| --gov1       | False                          | :x:                | Set for gov1 chains   |
| --call_data  | False                          | :x:                | Get encoded call data |
| --proxies    | None                           | :x:                | Get all proxies       |
| --output     | None                           | :heavy_check_mark: | Save output to ./data |

### ref_caller
###### Get the Call Data of an ongoing referendum
> .\chainstate.py --url wss://rpc.ibp.network/polkadot --ref_caller 707 --call_data  
> .\chainstate.py --url wss://rpc.ibp.network/polkadot --ref_caller 707 --call_data --output polkadot-ref-707-call-data.json
```
0x130503000100a10f0000020432050b0000275c0b12130000051f585f930903000101002f944a1d1c5688dd06bc0335fb0bb058fa7fb2805a4247047dbbbc6c15121bc900
```

###### Show the call that is being made
> .\chainstate.py --url wss://rpc.ibp.network/kusama --ref_caller 391  
> .\chainstate.py --url wss://rpc.ibp.network/kusama --ref_caller 391 --output kusama-ref-391-call.json
```json
{
    "call_index": "0x1208",
    "call_function": "void_spend",
    "call_module": "Treasury",
    "call_args": [
        {
            "name": "index",
            "type": "SpendIndex",
            "value": 3
        }
    ],
    "call_hash": "0xe83b5bd477e5c79e3f799310ae83788a955169f7900d65cbf5e1f406d793dae1"
}
```
---
### proxies
###### Get all proxies from chains determines in --url
> .\chainstate.py --url wss://rpc.ibp.network/polkadot --proxies  
> .\chainstate.py --url wss://rpc.ibp.network/kusama --proxies  
> .\chainstate.py --url wss://hydradx-rpc.dwellir.com --proxies  
> .\chainstate.py --url wss://sys.ibp.network/statemint --proxies  
> .\chainstate.py --url wss://acala-rpc.dwellir.com --proxies  
