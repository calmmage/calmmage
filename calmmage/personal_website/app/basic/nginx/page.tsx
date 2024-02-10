export default function Page() {
    return (
        <div>
            <h1>NGINX Configuration Instructions</h1>

            <h2>Generating New SSL Certificate</h2>
            <p>Launch Admin PowerShell:</p>
            <pre>Start PowerShell as Administrator</pre>
            <p>Run the following command:</p>
            <pre>certbot certonly --standalone -d calmmage.com</pre>

            <h2>Port Forwarding</h2>
            <p>Access your router settings:</p>
            <ul>
                <li>Go to <a href="http://192.168.1.1">192.168.1.1</a></li>
                <li>Navigate to Advanced Settings - Security - Port Forwarding</li>
            </ul>

            <h2>Adding New Subdomain Routing</h2>
            <p>Open PowerShell and navigate to your NGINX directory:</p>
            <pre>cd 'K:/Program Files/nginx'</pre>
            <p>Edit NGINX Configuration:</p>
            <ul>
                <li>Path to NGINX conf: 'K:/Program Files/nginx/conf/nginx.conf'</li>
                <li>Add/Edit server blocks as needed</li>
                <li>Save changes</li>
            </ul>
            <p>Restart NGINX:</p>
            <pre>Start PowerShell as Administrator</pre>
            <pre>nginx -s reload</pre>

            <h2>Setup domain calmmage.com</h2>
            <p><a href="https://apple-emu-f57h.squarespace.com/config/domains/managed/calmmage.com/dns-settings" target="_blank" rel="noopener noreferrer">https://apple-emu-f57h.squarespace.com/config/domains/managed/calmmage.com/dns-settings</a></p>

            <h1>This page</h1>
            <p>The file is K:/work/calmmage_com/help.html</p>
            <p>The main page is at calmmage.com </p>
            <p>The file is K:/work/calmmage_com/index.html</p>
            <p>Maybe redirect this endpoint there as well? </p>
        </div>
    );
}