### 描述
这是一个定时自动发送微信消息的脚本

### 参数介绍：

> optional arguments:  
  -h, --help     show this help message and exit  
  --r            是否使用上次的记录  
  --show_r       查看上次的记录  
  --time TIME    发送时间，格式为: 12:00:00  
  --delay DELAY  提前 or 延迟 多少秒发送，满了就减去，快了就加上  
  --who WHO      发送给谁，例如 张三  
  --msg MSG      消息内容，例如 今天天气真好  


time、delay、who、msg必须一起使用。  
 
`pc端时间一般有误差。可以进入 https://time.is/zh/， 点击左上角 TIME.IS logo，可以查看本机时间差距。  
慢了就将 delay 设置为负数，快了就设置为正数。如下所示:`

![](img/time_show.png)
 
> 示例：  

```shell script
# 发送一条消息
wechat_auto.py --time=12:00:00 --delay=-0.3 --who=文件传输助手 --msg=今天天气真不错  
# 执行上一次的命令
wechat_auto.py --r
# 查看上一次的消息
wechat_auto.py --sr 
```

 
 