# MachineHacking
## Step1:
### Nmap 
```sh
$ nmap -sV -sC -oA nmap <host>
```
## Step2:
If it works on a web browser, then we are going to use `Burp`.

## Step3:
If website is avilable and intercept is on, we use `Virtual Host Routing`.  
In `burp` do `Proxy -> Intercept -> Host: <machine_name>.htb -> Forward`

## Step4:
### Dirb
```sh
$ dirb http://<host> -r -o tmd.dirb
```
Then check all the `dirb`'d links.  
If a link is successful move to Step5.

## Step5:
