import fastify from 'fastify';

const server = fastify();

server.get('/', async (request, reply) => {
    // return { hello: 'world' };
    return { message: 'Hello world' };
});

server.put('/', async (request, reply) => {
    return { message: request.body};
});

const start = async () => {
    try {
        await server.listen(3000);
        server.log.info(`server listening on 3000`); //  ${server.server.address().port}`);
        console.log(`server listening on 3000`);
    } catch (err) {
        server.log.error(err);
        console.error("Error starting server", err);
        process.exit(1);
    }
};
start();
