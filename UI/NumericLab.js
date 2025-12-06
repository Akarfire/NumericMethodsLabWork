
// Wait for the HTML file to be fully loaded before running the code
document.addEventListener("DOMContentLoaded", onFileLoaded);

let isResizingContent = false;

const minOptionsWidth = 460;
const minResultsWidth = 100;

let inputData = {

    //General  
    "n" : 15,
    "m" : 3000,
    
    "a_min" : 0,
    "a_max" : 1,

    "b_min" : 0,
    "b_max" : 1,
    
    "degradation_mode" : "Uniform",
    "concentrated_range_fraction" : 0.25,
    
    "experiment_count" : 100,
    
    "use_individual_ranges" : false,
    "individual_a_ranges" : new Array(),
    "individual_b_ranges" : new Array(),
    
    // Additional Algorithm Data
    "greedy_thrifty_stage" : 5,
    "thrifty_greedy_stage" : 5,

    "bkj_stage" : 5,
    "bkj_rank" : 2,
    
    // Non-organics
    "use_non_organics" : false,
    
    "k_min" : 5,
    "k_max" : 7,
    
    "na_min" : 0.21,
    "na_max" : 0.82,
    
    "n_min" : 1.5,
    "n_max" : 2.8,
    
    "reduce_min" : 0,
    "reduce_max" : 1,
    
    // Ripening
    "use_ripening" : false,
    
    "ripening_stages" : 5,
    
    "ripening_min" : 1,
    "ripening_max" : 1.15
}

function onFileLoaded()
{
    setupContentSplit();

    // Setting up option cards
    setupGeneralOptions();
    setupAdditionalOptions();
    setupNonOrganicsOptions();
    setupRipeningOptions();

    setupButtonsPanel();

    // Receiving messages
    window.py.receive((message) => {
        alert("Frontend got message:" + message);
    });
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
    const left_panel = document.getElementById('left-panel');
    const results_container = document.getElementById('results-container');

    const containerWidth = divider.parentElement.getBoundingClientRect().width;

    // Clamping options width
    if (width_percent * containerWidth < minOptionsWidth) width_percent = (minOptionsWidth / containerWidth);

    if ((1 - width_percent) * containerWidth < minResultsWidth) width_percent = (1 - (minResultsWidth / containerWidth));

    left_panel.style.flex = `0 0 ${width_percent * 100}%`;
    results_container.style.flex = `1`;
}


// Option cards

function setupGeneralOptions()
{
    const generalCard = document.getElementById("general-card");

    const experiment_count_input = document.getElementById("experiment_count_input");
    experiment_count_input.addEventListener("change", (event) => {
        inputData.experiment_count = Number(event.currentTarget.value);
    });
    const n_input = document.getElementById("n_input");
    n_input.addEventListener("change", (event) => {
        inputData.n = Number(event.currentTarget.value);
    });
    const m_input = document.getElementById("m_input");
    m_input.addEventListener("change", (event) => {
        inputData.m = Number(event.currentTarget.value);
    });

    const a_min_input = document.getElementById("a_min_input");
    a_min_input.addEventListener("change", (event) => {
        inputData.a_min = Number(event.currentTarget.value);
    });
    const a_max_input = document.getElementById("a_max_input");
    a_max_input.addEventListener("change", (event) => {
        inputData.a_max = Number(event.currentTarget.value);
    });
    const b_min_input = document.getElementById("b_min_input");
    b_min_input.addEventListener("change", (event) => {
        inputData.b_min = Number(event.currentTarget.value);
    });
    const b_max_input = document.getElementById("b_max_input");
    b_max_input.addEventListener("change", (event) => {
        inputData.b_max = Number(event.currentTarget.value);
    });

    const degradation_mode_input = document.getElementById("degradation_mode_input");
    degradation_mode_input.addEventListener("change", (event) => {
        inputData.degradation_mode = event.currentTarget.value;
    });
    const concentrated_range_fraction_input = document.getElementById("concentrated_range_fraction_input");
    concentrated_range_fraction_input.addEventListener("change", (event) => {
        inputData.concentrated_range_fraction = Number(event.currentTarget.value);
    });

    const use_individual_ranges_input = document.getElementById("use_individual_ranges_input");
    use_individual_ranges_input.addEventListener("change", (event) => {
        inputData.use_individual_ranges = event.currentTarget.checked;
    });
}

function setupAdditionalOptions()
{
    const additionalCard = document.getElementById("additional-card");
    const showCheckBox = document.getElementById("show-additional-options-checkbox");
    
    showCheckBox.addEventListener('change', (event) => {
        //if (event.currentTarget.checked) additionalCard.style.height = "450px";
        //else additionalCard.style.height = "200px";
    });

    //additionalCard.style.height = "200px";

    const greedy_thrifty_stage_input = document.getElementById("greedy_thrifty_stage_input");
    greedy_thrifty_stage_input.addEventListener("change", (event) => {
        inputData.greedy_thrifty_stage = Number(event.currentTarget.value);
    });
    const thrifty_greedy_stage_input = document.getElementById("thrifty_greedy_stage_input");
    thrifty_greedy_stage_input.addEventListener("change", (event) => {
        inputData.thrifty_greedy_stage = Number(event.currentTarget.value);
    });
    const bkj_stage_input = document.getElementById("bkj_stage_input");
    bkj_stage_input.addEventListener("change", (event) => {
        inputData.bkj_stage = Number(event.currentTarget.value);
    });
    const bkj_rank_input = document.getElementById("bkj_rank_input");
    bkj_rank_input.addEventListener("change", (event) => {
        inputData.bkj_rank = Number(event.currentTarget.value);
    });
    const ctg_stage_input = document.getElementById("ctg_stage_input");
    ctg_stage_input.addEventListener("change", (event) => {
        inputData.ctg_stage_input = Number(event.currentTarget.value);
    });
}

function setupNonOrganicsOptions()
{
    const nonOrganicCard = document.getElementById("non-organic-card");
    const useCheckBox = document.getElementById("use-non-organics-checkbox");
    
    useCheckBox.addEventListener('change', (event) => {
        inputData.use_non_organics = event.currentTarget.checked;
        //if (event.currentTarget.checked) nonOrganicCard.style.height = "450px";
        //else nonOrganicCard.style.height = "200px";
    });

    //nonOrganicCard.style.height = "200px";

    const k_min_input = document.getElementById("k_min_input");
    k_min_input.addEventListener("change", (event) => {
        inputData.k_min = Number(event.currentTarget.value);
    });
    const k_max_input = document.getElementById("k_max_input");
    k_max_input.addEventListener("change", (event) => {
        inputData.k_max = Number(event.currentTarget.value);
    });

    const na_min_input = document.getElementById("na_min_input");
    na_min_input.addEventListener("change", (event) => {
        inputData.na_min = Number(event.currentTarget.value);
    });
    const na_max_input = document.getElementById("na_max_input");
    na_max_input.addEventListener("change", (event) => {
        inputData.na_max = Number(event.currentTarget.value);
    });

    const n_min_input = document.getElementById("n_min_input");
    n_min_input.addEventListener("change", (event) => {
        inputData.n_min = Number(event.currentTarget.value);
    });
    const n_max_input = document.getElementById("n_max_input");
    n_max_input.addEventListener("change", (event) => {
        inputData.n_max = Number(event.currentTarget.value);
    });

    const reduce_min_input = document.getElementById("reduce_min_input");
    reduce_min_input.addEventListener("change", (event) => {
        inputData.reduce_min = Number(event.currentTarget.value);
    });
    const reduce_max_input = document.getElementById("reduce_max_input");
    reduce_max_input.addEventListener("change", (event) => {
        inputData.reduce_max = Number(event.currentTarget.value);
    });
}

function setupRipeningOptions()
{
    const ripeningCard = document.getElementById("ripening-card");
    const useCheckBox = document.getElementById("use-ripening-checkbox");
    
    useCheckBox.addEventListener('change', (event) => {
        inputData.use_ripening = event.currentTarget.checked;
        //if (event.currentTarget.checked) ripeningCard.style.height = "450px";
        //else ripeningCard.style.height = "200px";
    });

    //ripeningCard.style.height = "200px";

    const ripening_stages_input = document.getElementById("ripening_stages_input");
    ripening_stages_input.addEventListener("change", (event) => {
        inputData.ripening_stages = Number(event.currentTarget.value);
    });

    const ripening_min_input = document.getElementById("ripening_min_input");
    ripening_min_input.addEventListener("change", (event) => {
        inputData.ripening_min = Number(event.currentTarget.value);
    });

    const ripening_max_input = document.getElementById("ripening_max_input");
    ripening_max_input.addEventListener("change", (event) => {
        inputData.ripening_max = Number(event.currentTarget.value);
    });
}


function setupButtonsPanel()
{
    const runButton = document.getElementById("run-button");
    runButton.addEventListener("click", () => {
        window.py.send({ "input_data" : inputData });
    });
}