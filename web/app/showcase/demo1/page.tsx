export default function Page() {
    return (
        <div className="prose prose-sm prose-invert max-w-none">
            <div style={{
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center'
            }}>
                <h1 className="text-xl font-bold">Petr Lavrov Projects Showcase</h1>
            </div>
            <div className="w-full"
                 style={{border: '2px dotted #101', padding: '10px'}}>
                <iframe scrolling="no"
                        src="/showcase/demo1-fast-circle/index.html"
                        style={{width: '100%', height: '600px', border: 'none'}}
                        title="Demo 1"
                ></iframe>
            </div>
        </div>
    );
}
