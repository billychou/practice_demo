local util = require "util"

local function tc()

  local uri = ngx.var.uri
  uri = string.gsub(uri, "/$", "")
  local ip = util.get_client_ip()

  local rediskey = 'crawler#'..uri..'#'.. ip
  ngx.var.crawler_key = rediskey
  args = ngx.encode_args( { key = rediskey })
  path = '/@getflag?' .. args
  local res = ngx.location.capture(path,{method = ngx.HTTP_GET,copy_all_vars=true})
  local flag = res.body

  return flag

end

local status,ret = pcall(tc)

ret = string.gsub(ret, "^%s*(.-)%s*$", "%1")

if ret == 's' then
  if ngx.req.get_method() == 'GET' then
    local logdata = 'request_honey'
    ngx.log(ngx.WARN,logdata)
  elseif ngx.req.get_method() == 'POST' then
    ngx.req.read_body()
    local postdata = ngx.req.get_body_data()
    local logdata = 'request_honey "' .. postdata .. '"'
    ngx.log(ngx.WARN,logdata)
  end
  ngx.var.crawler_status = "crawler_honey"
  ngx.exec("@request_honey")
else
  ngx.var.crawler_status = "crawler_allow"
  ngx.exec("@request_allow")
end