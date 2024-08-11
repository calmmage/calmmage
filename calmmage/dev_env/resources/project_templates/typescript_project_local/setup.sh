npm install typescript
# fastify
npx tsc init
npm install fastify
npm install @types/node

# definig the simple curl to Test the server:
test_server() {
    local port=${1:-3000}
    curl "localhost:${port}" -X PUT -d '{"content":"asd"}' -H 'content-type:application/json'
}

# Call the function with the port number
# test_server 3000
