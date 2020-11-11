[![FivexL](https://releases.fivexl.io/fivexlbannergit.jpg)](https://fivexl.io/)

# Tools for HashiCorp Vault access audit


## How to setup

```
bash source.sh
source env/bin/activate
```

## How to run

Pre-process dataset

```
> curl -OL https://raw.githubusercontent.com/hashicorp/vault-guides/master/monitoring-troubleshooting/vault-audit.log
> python3 vault_etl.py vault-audit.log vault-audit.gzip
Processing vault-audit.log and storing result to vault-audit.gzip
vault-audit.log is a file. Parse it
Reading vault-audit.log
Resulting data frame
                            time      type                                  auth.client_token  ... auth.metadata.username response.auth.metadata.username                                         error
0   2020-04-30T14:27:10.6656485Z  response  hmac-sha256:bd6dd75911924ab82f9dcfa7adae6b8214...  ...                    NaN                             NaN                                           NaN
0   2020-04-30T14:27:10.7416596Z   request  hmac-sha256:bd6dd75911924ab82f9dcfa7adae6b8214...  ...                    NaN                             NaN                                           NaN
0   2020-04-30T14:27:10.7553994Z  response  hmac-sha256:bd6dd75911924ab82f9dcfa7adae6b8214...  ...                    NaN                             NaN                                           NaN
0   2020-04-30T14:27:10.9021354Z   request  hmac-sha256:bd6dd75911924ab82f9dcfa7adae6b8214...  ...                    NaN                             NaN                                           NaN
0   2020-04-30T14:27:10.9200303Z  response  hmac-sha256:bd6dd75911924ab82f9dcfa7adae6b8214...  ...                    NaN                             NaN                                           NaN
..                           ...       ...                                                ...  ...                    ...                             ...                                           ...
0   2020-04-30T19:12:58.5648483Z  response                                                NaN  ...                    NaN                             NaN  1 error occurred:\n\t* permission denied\n\n
0   2020-04-30T19:32:00.7744629Z   request                                                NaN  ...                    NaN                             NaN                                           NaN
0   2020-04-30T19:32:00.9207237Z  response  hmac-sha256:518960cc83c46311ea2d5a3a22cdc4b4aa...  ...             lab-user-4                      lab-user-4                                           NaN
0   2020-04-30T19:35:23.1771431Z   request                                                NaN  ...                    NaN                             NaN                                           NaN
0   2020-04-30T19:35:23.2895529Z  response  hmac-sha256:0cd939fcb7c61532ddbcc2b1992a7bbc74...  ...             lab-user-5                      lab-user-5                                           NaN

[1397 rows x 29 columns]
Writing to vault-audit.gzip
```
Explore dataset

```
> python3
Python 3.8.5 (default, Jul 28 2020, 12:59:40) 
[GCC 9.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import pandas
>>> df = pandas.read_parquet('./vault-audit.gzip')
>>> print(df)
                            time      type                                  auth.client_token  ... auth.metadata.username response.auth.metadata.username                                         error
0   2020-04-30T14:27:10.6656485Z  response  hmac-sha256:bd6dd75911924ab82f9dcfa7adae6b8214...  ...                   None                            None                                          None
0   2020-04-30T14:27:10.7416596Z   request  hmac-sha256:bd6dd75911924ab82f9dcfa7adae6b8214...  ...                   None                            None                                          None
0   2020-04-30T14:27:10.7553994Z  response  hmac-sha256:bd6dd75911924ab82f9dcfa7adae6b8214...  ...                   None                            None                                          None
0   2020-04-30T14:27:10.9021354Z   request  hmac-sha256:bd6dd75911924ab82f9dcfa7adae6b8214...  ...                   None                            None                                          None
0   2020-04-30T14:27:10.9200303Z  response  hmac-sha256:bd6dd75911924ab82f9dcfa7adae6b8214...  ...                   None                            None                                          None
..                           ...       ...                                                ...  ...                    ...                             ...                                           ...
0   2020-04-30T19:12:58.5648483Z  response                                               None  ...                   None                            None  1 error occurred:\n\t* permission denied\n\n
0   2020-04-30T19:32:00.7744629Z   request                                               None  ...                   None                            None                                          None
0   2020-04-30T19:32:00.9207237Z  response  hmac-sha256:518960cc83c46311ea2d5a3a22cdc4b4aa...  ...             lab-user-4                      lab-user-4                                          None
0   2020-04-30T19:35:23.1771431Z   request                                               None  ...                   None                            None                                          None
0   2020-04-30T19:35:23.2895529Z  response  hmac-sha256:0cd939fcb7c61532ddbcc2b1992a7bbc74...  ...             lab-user-5                      lab-user-5                                          None

[1397 rows x 29 columns]
>>>
>>>
>>> # Responses and requests
>>> df[['type']].value_counts()
type    
response    699
request     698
dtype: int64
>>> 
>>>
>>> # Count display names
>>> df[['auth.display_name']].value_counts()
auth.display_name  
token                  453
token-lab-admins       423
userpass-lab-user-7    144
userpass-lab-user-3     74
userpass-lab-user-5     33
root                    21
userpass-lab-user-1     11
approle                  8
userpass-lab-user-4      1
dtype: int64
>>> 
>>> # Count display names with operations
>>> df[['auth.display_name', 'request.path', 'request.operation']].value_counts()
auth.display_name    request.path                    request.operation
token                kv-v2/metadata/                 list                 176
                     sys/internal/ui/mounts/kv-v2    read                 176
userpass-lab-user-7  auth/userpass/login/lab-user-7  update               102
userpass-lab-user-3  auth/userpass/login/lab-user-3  update                74
token-lab-admins     totp/code/my-key                read                  50
                                                                         ... 
                     transit/encrypt/my-key-31       create                 2
                     transit/encrypt/my-key-30       create                 2
                     transit/encrypt/my-key-3        create                 2
root                 sys/audit/file                  update                 1
userpass-lab-user-4  auth/userpass/login/lab-user-4  update                 1
Length: 232, dtype: int64
>>> 
>>> 
>>> # Request operations
>>> df[['request.operation']].value_counts()
request.operation
update               573
read                 346
create               274
list                 184
delete                20
dtype: int64
>>> 
>>> 
>>> # Filter out all errors
>>> df.query('error.notnull()', engine='python')[['error', 'auth.display_name', 'request.path', 'request.operation']]
                                          error auth.display_name                      request.path request.operation
0                             permission denied              None  sys/internal/ui/mounts/kv-v2/lab              read
0                          missing client token              None      sys/internal/ui/mounts/kv-v2              read
0   1 error occurred:\n\t* unsupported path\n\n             token                     approle/role/              list
0                             permission denied              None                        sys/mounts              read
0  1 error occurred:\n\t* permission denied\n\n              None                        sys/mounts              read
0                             permission denied              None                        sys/mounts              read
0  1 error occurred:\n\t* permission denied\n\n              None                        sys/mounts              read
>>> 
>>> 
>>> # Count ip addresses
>>> df['request.remote_address'].value_counts()
10.10.42.222    1389
10.10.42.210       4
10.10.42.213       2
10.10.42.212       2
Name: request.remote_address, dtype: int64
>>> 
>>> 
>>> # All operations done by root
>>> df.loc[df['auth.display_name'] == 'root'][['time', 'type', 'request.path', 'request.operation']]
                           time      type                      request.path request.operation
0  2020-04-30T14:27:10.6656485Z  response                    sys/audit/file            update
0  2020-04-30T14:27:10.7416596Z   request           sys/policies/acl/admins            update
0  2020-04-30T14:27:10.7553994Z  response           sys/policies/acl/admins            update
0  2020-04-30T14:27:10.9021354Z   request         sys/policies/acl/lab-user            update
0  2020-04-30T14:27:10.9200303Z  response         sys/policies/acl/lab-user            update
0  2020-04-30T14:27:11.0097064Z   request           auth/token/roles/admins            create
0  2020-04-30T14:27:11.0208794Z  response           auth/token/roles/admins            create
0  2020-04-30T14:27:11.1196533Z   request          auth/token/create/admins            update
0  2020-04-30T14:27:11.1801344Z  response          auth/token/create/admins            update
0  2020-04-30T15:05:26.8671147Z   request            auth/token/lookup-self              read
0  2020-04-30T15:05:26.8695668Z  response            auth/token/lookup-self              read
0  2020-04-30T15:05:39.8725426Z   request      sys/internal/ui/mounts/kv-v2              read
0  2020-04-30T15:05:39.8748566Z  response      sys/internal/ui/mounts/kv-v2              read
0  2020-04-30T15:05:39.8879207Z   request                   kv-v2/metadata/              list
0  2020-04-30T15:05:39.8897394Z  response                   kv-v2/metadata/              list
0  2020-04-30T15:05:44.3467807Z   request  sys/internal/ui/mounts/kv-v2/lab              read
0  2020-04-30T15:05:44.3485479Z  response  sys/internal/ui/mounts/kv-v2/lab              read
0    2020-04-30T15:05:44.35361Z   request               kv-v2/metadata/lab/              list
0  2020-04-30T15:05:44.3548863Z  response               kv-v2/metadata/lab/              list
0  2020-04-30T15:09:05.4278888Z   request                 auth/token/create            update
0  2020-04-30T15:09:05.4643868Z  response                 auth/token/create            update
>>> 
>>> 
>>> # Fix arrays
>>> import numpy as numpy
>>> for column in df.columns:
...     df[column] = df[column].apply(lambda x: ",".join(x) if isinstance(x, numpy.ndarray) else x)
... 
>>> 
>>> # Check policies used
>>> df[['auth.token_policies']].value_counts()
auth.token_policies
admins,default         876
default,lab-user       263
root                    21
default                  8
dtype: int64
>>> 
>>> 
>>> # Visualise df
>>> from pandasgui import show
>>> show(df)
<pandasgui.gui.PandasGui object at 0x7facc3db2af0>
>>> 

```
