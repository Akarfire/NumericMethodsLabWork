
// Wait for the HTML file to be fully loaded before running the code
document.addEventListener("DOMContentLoaded", onFileLoaded);

let isResizingContent = false;

const minOptionsWidth = 360;
const minResultsWidth = 100;

let inputData = {

    //General  
    n : 15,
    m : 3000,
    
    a_min : 0,
    a_max : 1,

    b_min : 0,
    b_max : 1,
    
    degradation_mode : DegradationMode.UNIFORM,
    concentrated_range_fraction : 0.25,
    
    experiment_count : 100,
    
    use_individual_ranges : False,
    individual_a_ranges : Array,
    individual_b_ranges : Array,
    
    // Additional Algorithm Data
    greedy_thrifty_stage : 5,
    thrifty_greedy_stage : 5,

    bkj_stage : 5,
    bkj_rank : 2,
    
    // Non-organics
    use_non_organics : False,
    
    k_min : 5,
    k_max : 7,
    
    na_min : 0.21,
    na_max : 0.82,
    
    n_min : 1.5,
    n_max : 2.8,
    
    reduce_min : 0,
    reduce_max : 1,
    
    // Ripening
    use_ripening : False,
    
    ripening_stages : 5,
    
    ripening_min : 1,
    ripening_max : 1.15
}

function onFileLoaded()
{
    setupContentSplit();

    setupGeneralOptions();
    setupAdditionalOptions();
    setupNonOrganicsOptions();
    setupRipeningOptions();
}


// Content Split

function setupContentSplit()
{
    const divider = document.getElementById('content-divider');

    divider.addEventListener('mousedown', () => {
        isResizingContent = true;
        document.body.style.cursor = 'col-resize';
    });

    document.addEventListener('mousemove', (e) => {
        if (!isResizingContent) return;

        const containerWidth = divider.parentElement.getBoundingClientRect().width;
        const optionsWidth = e.clientX / containerWidth;

        contentSplitSetPercent(optionsWidth);
    });

    document.addEventListener('mouseup', () => {
        isResizingContent = false;
        document.body.style.cursor = 'default';
    });

    contentSplitSetPercent(0.3);
}

function contentSplitSetPercent(width_percent)
{
    const divider = document.getElementById('content-divider');
    const options_container = document.getElementById('options-container');
    const content_containertPanel = document.getElementById('results-container');

    const containerWidth = divider.parentElement.getBoundingClientRect().width;

    // Clamping options width
    if (width_percent * containerWidth < minOptionsWidth) width_percent = (minOptionsWidth / containerWidth);

    if ((1 - width_percent) * containerWidth < minResultsWidth) width_percent = (1 - (minResultsWidth / containerWidth));

    options_container.style.flex = `0 0 ${width_percent * 100}%`;
    content_containertPanel.style.flex = `1`;
}


function setupGeneralOptions()
{
    const generalCard = document.getElementById("general-card");
}

function setupAdditionalOptions()
{
    const additionalCard = document.getElementById("additional-card");
    const showCheckBox = document.getElementById("show-additional-options-checkbox");
    
    showCheckBox.addEventListener('change', (event) => {

        if (event.currentTarget.checked) additionalCard.style.height = "450px";
        else additionalCard.style.height = "200px";
    });

    additionalCard.style.height = "200px";
}

function setupNonOrganicsOptions()
{
    const nonOrganicCard = document.getElementById("non-organic-card");
    const useCheckBox = document.getElementById("use-non-organics-checkbox");
    
    useCheckBox.addEventListener('change', (event) => {

        if (event.currentTarget.checked) nonOrganicCard.style.height = "450px";
        else nonOrganicCard.style.height = "200px";
    });

    nonOrganicCard.style.height = "200px";
}

function setupRipeningOptions()
{
    const ripeningCard = document.getElementById("ripening-card");
    const useCheckBox = document.getElementById("use-ripening-checkbox");
    
    useCheckBox.addEventListener('change', (event) => {

        if (event.currentTarget.checked) ripeningCard.style.height = "450px";
        else ripeningCard.style.height = "200px";
    });

    ripeningCard.style.height = "200px";
}