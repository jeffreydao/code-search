## Node and Vue Setup (reload shell after done)
```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.0/install.sh | bash
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
nvm install 22
npm install -g @vue/cli
npm install axios

node -v # should print `v22.11.0`
npm -v # should print `10.9.0`
vue -V
```

## Python venv
1. Open command pallete
2. Create python environment ---> venv
3. `pip install "fastapi[standard]" sqlmodel`

## Starting new Vue project
`vue create .`

## Running

`fastapi dev main.py`

`npm run serve`