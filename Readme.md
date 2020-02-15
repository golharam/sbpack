# sbpack

![](https://github.com/kaushik-work/sbpack/workflows/Tests/badge.svg)

Upload CWL apps to any Seven Bridges powered platform. Resolves linked processes, schemadefs and `$include`s and
 `$import`s.

## Installation

(It is good practice to install Python programs in a virtual environment. [pipx] is a very effective tool for
 installing command line Python tools in isolated environments)

[pipx]: https://github.com/pipxproject/pipx

`sbpack` needs Python 3.6 or later

```
pip3 install pipx  # in case you don't have pipx
pipx ensurepath # ensures CLI application directory is on your $PATH
pipx install --spec git+https://github.com/kaushik-work/sbpack.git sbpack
# use pipx upgrade ... if upgrading an existing install
```

## Usage
```
Usage
   sbpack <profile> <id> <cwl>
 
where:
  <profile> refers to a SB platform profile as set in the SB API credentials file.
  <id> takes the form {user}/{project}/{app_id} which installs (or updates) 
       "app_id" located in "project" of "user".
  <cwl> is the path to the main CWL file to be uploaded. This can be a remote file.
```
 
## Uploading workflows defined remotely

`sbpack` handles local paths and remote URLs in a principled manner. This means that
`sbpack` will handle packing and uploading a local workflow that links to a remote workflow
which itself has linked workflows. It will therefore also handle packing a fully 
remote workflow.

For example, to pack and upload the workflow located at `https://github.com/Duke-GCB/GGR-cwl/blob/master/v1.0/ATAC-seq_pipeline/pipeline-se.cwl`
go to the `raw` button and use that URL, like:

```bash
sbpack sbg kghosesbg/sbpla-31744/ATAC-seq-pipeline-se https://raw.githubusercontent.com/Duke-GCB/GGR-cwl/master/v1.0/ATAC-seq_pipeline/pipeline-se.cwl
``` 

## Credentials file and profiles

If you use the SBG API you already have an API configuration file. If
not, you should create one. It is located in 
`~/.sevenbridges/credentials`.

Briefly, each section in the SBG configuration file (e.g. `[cgc]`) is a 
profile name and has two entries. The end-point and an authentication
token, which you get from your developer tab on the platform.

```
[sbg-us]
api_endpoint = https://api.sbgenomics.com/v2
auth_token   = <dev token here>

[sbg-eu]
api_endpoint = https://eu-api.sbgenomics.com/v2
auth_token   = <dev token here>

[sbg-china]
api_endpoint = https://api.sevenbridges.cn/v2
auth_token   = <dev token here>

[cgc]
api_endpoint = https://cgc-api.sbgenomics.com/v2
auth_token   = <dev token here>

[cavatica]
api_endpoint = https://cavatica-api.sbgenomics.com/v2
auth_token   = <dev token here>
```

You can have several profiles on the same platform if, for example, you 
are an enterprise user and you belong to several divisions. Please refer
to the API documentation for more detail.
