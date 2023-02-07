## Set up production
- B1: Generate key pair by code below and then enter file or password if you want (optional)

```sh
ssh-keygen -t rsa -b 4096
```
- B2: Copy text in <key-pair-file-name>.pub

- B3: Go to aws ec2 and choose "Key Pair" in "Network & Security" section

- B4: In actions button, choose "import key pair", then paste your keypair in "Public key contents text box" and input your keypair name

- B5: Go to instances section and create ec2 instances with linux version.

- B6: In "key pair (Login)" when creating ec2 instance, you choose Key pair name which was created before.

- B7: Verify and wait instance until running.

- B8: In terminal, go to the location where contain keypair file

- B9: Run
```sh
ssh-add <key-pair-file-name>
ssh ec2-user@<your-public-ip-instance>
```
- B10: Install git and docker in [Here](https://github.com/ClarkLe01/project_management/blob/main/docs/install-docker-aws.md)
- B11: Git clone repository
- B12: Create environmnet file production in [Here](https://github.com/ClarkLe01/project_management/blob/main/README.md)
