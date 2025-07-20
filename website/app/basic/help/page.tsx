export default function Page() {
    return (
        <div style={{ fontFamily: 'Arial, sans-serif', padding: '20px' }}>
            <h1 style={{ color: '#333' }}>Welcome to the Help Page</h1>
            <p>This page provides information about my hosting and other related resources. Please find the relevant links below:</p>
            <h3>Personal Resources</h3>
            <ul>
                <li><a href="http://coolify.calmmage.com" target="_blank" rel="noopener noreferrer">Coolify</a> - My personal deployment and container management tool</li>
                <li><a href="http://n8n.calmmage.com" target="_blank" rel="noopener noreferrer">N8N</a> - My personal automation tool</li>
            </ul>
            <h3>Public Resources</h3>
            <ul>
                <li><a href="http://hetzner.calmmage.com" target="_blank" rel="noopener noreferrer">Hetzner</a> - A publicly available Coolify instance</li>
            </ul>
            <h3>Contact</h3>
            <p>For any queries or concerns, feel free to <a href="mailto:petrlavrov@calmmage.com">email me</a>.</p>
        </div>
    );
}