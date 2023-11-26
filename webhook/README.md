# Usage

Activate webhook server with following command in ~/resume-site-2:

```
$ webhook -hooks /root/resume-site-2/webhook/hooks.json -secure -cert /etc/letsencrypt/live/andersjuengst.com/fullchain.pem -key /etc/letsencrypt/live/andersjuengst.com/privkey.pem -hotreload
```

set github action env var to https://andersjuengst.com:9000/hooks/redeploy
