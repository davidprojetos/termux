# Hub de projetos TERMUX

### Config SSH
## Email
```sh
  ssh-keygen -t rsa -b 4096 -C "davidffsousaff@gmail.com"
```

## Get key
```sh
  cat ~/.ssh/id_rsa.pub
```
## Config git
```sh
  git init
  git clone git@github.com:davidprojetos/?.git
  git push --set-upstream origin main
```

### Git Pull
```sh
  git pull
```

### Git Push
```sh
  git add . && git commit -m "add " && git push
```

