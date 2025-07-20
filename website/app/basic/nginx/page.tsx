const NGINXConfigPath = `K:/Program Files/nginx/conf/nginx.conf`;

export default function Page() {
    return (
        <div className="p-8">
            <h1 className="text-3xl font-bold mb-4">NGINX Configuration Instructions</h1>

            <div className="mb-32 grid text-center lg:max-w-5xl lg:w-full lg:mb-0 lg:grid-cols-4 lg:text-left">
                <div className="group rounded-lg border border-transparent px-5 py-4 transition-colors hover:border-gray-300 hover:bg-gray-100 hover:dark:border-neutral-700 hover:dark:bg-neutral-800/30">
                    <h2 className="mb-3 text-2xl font-semibold">Generating New SSL Certificate</h2>
                    <p className="m-0 max-w-[30ch] text-sm opacity-50">
                        Launch Admin PowerShell and run:
                        <code className="block bg-gray-800 p-2 rounded mt-2">certbot certonly --standalone -d calmmage.com</code>
                    </p>
                </div>

                <div className="group rounded-lg border border-transparent px-5 py-4 transition-colors hover:border-gray-300 hover:bg-gray-100 hover:dark:border-neutral-700 hover:dark:bg-neutral-800/30">
                    <h2 className="mb-3 text-2xl font-semibold">Port Forwarding</h2>
                    <p className="m-0 max-w-[30ch] text-sm opacity-50">
                        Access your router at <a href="http://192.168.1.1" className="text-blue-500 underline">192.168.1.1</a>, navigate to Port Forwarding.
                    </p>
                </div>

                <div className="group rounded-lg border border-transparent px-5 py-4 transition-colors hover:border-gray-300 hover:bg-gray-100 hover:dark:border-neutral-700 hover:dark:bg-neutral-800/30">
                    <h2 className="mb-3 text-2xl font-semibold">Adding New Subdomain Routing</h2>
                    <p className="m-0 max-w-[30ch] text-sm opacity-50">
                        Edit NGINX Config at {NGINXConfigPath} and reload NGINX.
                        <code className="block bg-gray-800 p-2 rounded mt-2">nginx -s reload</code>
                    </p>
                </div>

                <div className="group rounded-lg border border-transparent px-5 py-4 transition-colors hover:border-gray-300 hover:bg-gray-100 hover:dark:border-neutral-700 hover:dark:bg-neutral-800/30">
                    <h2 className="mb-3 text-2xl font-semibold">Setup domain calmmage.com</h2>
                    <p className="m-0 max-w-[30ch] text-sm opacity-50">
                        Configure DNS settings at: <a href="https://apple-emu-f57h.squarespace.com/config/domains/managed/calmmage.com/dns-settings" className="text-blue-500 underline" target="_blank" rel="noopener noreferrer">Squarespace DNS Settings</a>
                    </p>
                </div>
            </div>
        </div>
    );
}
