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

### Configuração do .bashrc termux
```sh
export ANDROID_HOME="$PREFIX/opt/Android/sdk"
export PATH="$PATH:$ANDROID_HOME/cmdline-tools/latest/bin"
export JAVA_HOME=/data/data/com.termux/files/usr/lib/jvm/java-17-openjdk
export "PATH=$PATH:$PREFIX/opt/gradle/bin"
```

```sh
  source ~/.bashrc
```

### Adicionar ao aqrquivo gradle.properties no projeto cordova /plataforms/android

```sh
  cordova create xxx xxx.xxx.xxx "XXX Aaa"
```

```sh
  cordova platform add android
  cordova platform ls
```

```sh
android.aapt2FromMavenOverride=/data/data/com.termux/files/usr/opt/Android/sdk/build-tools/34.0.0/aapt2
```

```sh
  cordova build android
  cp /data/data/com.termux/files/home/termux/projetoscordova/xxx/platforms/android/app/build/outputs/apk/debug/app-debug.apk ~/storage/downloads

```

