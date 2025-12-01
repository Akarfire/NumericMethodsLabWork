
// Wait for the HTML file to be fully loaded before running the code
document.addEventListener("DOMContentLoaded", onFileLoaded);

let isResizingContent = false;

const minOptionsWidth = 15;
const minResultsWidth = 25;

function onFileLoaded()
{
    const divider = document.getElementById('content-divider');
    const options_container = document.getElementById('options-container');
    const content_containertPanel = document.getElementById('results-container');

    divider.addEventListener('mousedown', () => {
        isResizingContent = true;
        document.body.style.cursor = 'col-resize';
    });

    document.addEventListener('mousemove', (e) => {
        if (!isResizingContent) return;

        const containerWidth = divider.parentElement.getBoundingClientRect().width;
        const optionsWidth = e.clientX / containerWidth * 100;

        // Clamping options width
        if (optionsWidth < minOptionsWidth) optionsWidth = minOptionsWidth;

        if (100 - optionsWidth < minResultsWidth) optionsWidth = 100 - minResultsWidth;

        options_container.style.flex = `0 0 ${optionsWidth}%`;
        content_containertPanel.style.flex = `1`;
    });

    document.addEventListener('mouseup', () => {
        isResizingContent = false;
        document.body.style.cursor = 'default';
    });
}