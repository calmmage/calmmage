export default function Page() {
    return (
        <div className="p-8">
            <h1 className="text-3xl font-bold mb-4">NGINX Configuration Instructions</h1>

            <h2 className="text-2xl font-semibold mt-6 mb-2">Generating New SSL Certificate</h2>
            <p className="mb-1">Launch Admin PowerShell:</p>
            <pre className="bg-gray-200 p-4 rounded">Start PowerShell as Administrator</pre>
            <p className="mb-1">Run the following command:</p>
            <pre className="bg-gray-200 p-4 rounded mb-4">certbot certonly --standalone -d calmmage.com</pre>

            <h2 className="text-2xl font-semibold mt-6 mb-2">Port Forwarding</h2>
            <p className="mb-1">Access your router settings:</p>
            <ul className="list-disc pl-8 mb-4">
                <li>Go to <a href="http://192.168.1.1" className="text-blue-500 underline">192.168.1.1</a></li>
                <li>Navigate to Advanced Settings - Security - Port Forwarding</li>
            </ul>

            <h2 className="text-2xl font-semibold mt-6 mb-2">Adding New Subdomain Routing</h2>
            <p className="mb-1">Open PowerShell and navigate to your NGINX directory:</p>
            <pre className="bg-gray-200 p-4 rounded">cd 'K:/Program Files/nginx'</pre>
            <p className="mb-1">Edit NGINX Configuration:</p>
            <ul className="list-disc pl-8 mb-4">
                <li>Path to NGINX conf: 'K:/Program Files/nginx/conf/nginx.conf'</li>
                <li>Add/Edit server blocks as needed</li>
                <li>Save changes</li>
            </ul>
            <p className="mb-1">Restart NGINX:</p>
            <pre className="bg-gray-200 p-4 rounded mb-1">Start PowerShell as Administrator</pre>
            <pre className="bg-gray-200 p-4 rounded mb-4">nginx -s reload</pre>

            <h2 className="text-2xl font-semibold mt-6 mb-2">Setup domain calmmage.com</h2>
            <p className="mb-4"><a href="https://apple-emu-f57h.squarespace.com/config/domains/managed/calmmage.com/dns-settings" className="text-blue-500 underline" target="_blank" rel="noopener noreferrer">DNS Settings</a></p>
        </div>
    );
}
