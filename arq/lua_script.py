publish_job_lua = """
local stream_key = KEYS[1]
local job_message_id_key = KEYS[2]
local job_id = ARGV[1]
local score = ARGV[2]
local job_message_id_expire_ms = ARGV[3]
local message_id = redis.call('xadd', stream_key, '*', 'job_id', job_id, 'score', score)
redis.call('set', job_message_id_key, message_id, 'px', job_message_id_expire_ms)
return message_id
"""

get_job_from_stream_lua = """
local stream_key = KEYS[1]
local job_message_id_key = KEYS[2]
local message_id = redis.call('get', job_message_id_key)
if message_id == false then
    return nil
end
local job = redis.call('xrange', stream_key, message_id, message_id)
if job == nil then
    return nil
end
return job[1]
"""