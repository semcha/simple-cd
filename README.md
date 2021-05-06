# simple-cd

Simple Continuous Deployment for Github written on Python, inspired by [ci-ninja](https://github.com/backmeupplz/ci-ninja).

## Usage
1. `git clone https://github.com/semcha/simple-cd.git` on the server
2. Install simple-cd service `sudo cp home/simple-cd/simple-cd.service /etc/systemd/system`
3. Add scripts with the name like `{repository-name}-master.sh` to `scripts` folder
4. Make sure the files are executable (like `sudo chmod +x {repository-name}-master.sh`)
5. Add Webhook from your GitHub repository to `http://{server-ip}:61439/simple-cd`
6. Run simple-cd service `sudo systemctl start simple-cd`

## Webhook example
![Webhook example](https://i.imgur.com/OwvgKbS.png)
