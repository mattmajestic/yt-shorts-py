function toggleVideo(section) {
    const dockerIframe = document.getElementById('docker-iframe');
    const blockchainIframe = document.getElementById('blockchain-iframe');

    if (section === 'docker') {
        dockerIframe.style.display = 'block';
        blockchainIframe.style.display = 'none';
    } else if (section === 'blockchain') {
        dockerIframe.style.display = 'none';
        blockchainIframe.style.display = 'block';
    }
}
