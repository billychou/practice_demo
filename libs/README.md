### 基础功能库
version: v0.1-dev

目前仅支持 Django

## 模块列表：

 * common：
  
   * config 基础配置
   
   * crypt 加解密
   
   * error 错误异常
   
   * gfw 文明用语
   
   * misc 工具模块
   
   * mixin 插件
   
   * borm biz-orm业务关系对象
   
   * cifa 客户端请求cifa解析
   
 * django：
  
   * cache 缓存：
     
     * combo_backend 复合缓存  
     * redis_backend redis缓存
     * sentinel_backend redis哨兵  
     
   * config 统一配置读取：
   
     * channel_conf aos-channel读取  
     * logger_conf 统一日志配置
     
   * gfw 文明用语模块
   
   * httpclient http请求模块
   
   * logger sys日志/handler
   
   * middleware 中间件
   
     * accesslog access日志搜集  
     * limit 限流模块
     * request_init 请求初始化/加解密  
     
   * misc 工具函数库
   
   * sender sms/email 发送
   
   * decorators 装饰器,签名校验，ip校验
   
   * vaild 正则校验器