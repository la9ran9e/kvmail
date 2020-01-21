box.cfg {
    listen = '127.0.0.1:3313',
    background = true,
    log = 'tarantool.log',
    pid_file = 'tarantool.pid'
}

local function bootstrap()
    local env = os.environ()
    box.schema.space.create('kv', {id = 999})
    box.space.kv:create_index('primary', {type = 'hash', parts = {1, 'string'}})
    box.schema.user.create(env['KV_USER'], { password = env['KV_PASS'] })
    box.schema.user.grant(env['KV_USER'], 'read,write,execute', 'universe')
end

box.once('app-2.2', bootstrap)