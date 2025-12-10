
// Wait for the HTML file to be fully loaded before running the code
document.addEventListener("DOMContentLoaded", onFileLoaded);

let isResizingContent = false;
let isResizingResults = false;
let isResizingInterpretation = false;

const minOptionsWidth = 460;
const minResultsWidth = 500;

const minPlotHeight = 100;
const minInterpretationHeight = 100;

let contentSplitWidth = 0;
let resultsSplitHeight = 0;

let isLoading = false;

let inputData = {

    //General  
    "n" : 15,
    "m" : 3000,
    
    "a_min" : 0.12,
    "a_max" : 0.22,

    "b_min" : 0.85,
    "b_max" : 1,
    
    "degradation_mode" : "UNIFORM",
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

let isInputCorrect = true;

function onFileLoaded()
{
    setupContentSplit();
    setupResultsSplit();

    // Setting up option cards
    setupGeneralOptions();
    setupAdditionalOptions();
    setupNonOrganicsOptions();
    setupRipeningOptions();

    setupButtonsPanel();

    // Receiving messages
    window.py.receive((message) => {
        data = JSON.parse(message);
        if (typeof data.results === "object")
        {
            showResults(data.results);
        }
    });

    window.addEventListener('resize', handleWindowResize);
}

function handleWindowResize()
{
    const content_divider = document.getElementById('content-divider');
    const content_containerWidth = content_divider.parentElement.getBoundingClientRect().width;

    contentSplitSetPercent(contentSplitWidth / content_containerWidth);

    // const results_divider = document.getElementById('results-divider');
    // const results_containerHeight = results_divider.parentElement.getBoundingClientRect().height;

    // resultsSplitSetPercent(resultsSplitHeight / results_containerHeight);
}

// Content Split

function setupContentSplit()
{
    const divider = document.getElementById('content-divider');

    const overlay = document.getElementById("plot-iframe-overlay");

    divider.addEventListener('mousedown', () => {
        isResizingContent = true;
        document.body.style.cursor = 'col-resize';

        overlay.style.pointerEvents = "auto";
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

        overlay.style.pointerEvents = "none";
    });

    const containerWidth = divider.parentElement.getBoundingClientRect().width;
    contentSplitSetPercent(minOptionsWidth / containerWidth);
}

function contentSplitSetPercent(width_percent)
{
    const left_panel = document.getElementById('left-panel');
    const results_container = document.getElementById('results-container');

    const divider = document.getElementById('content-divider');
    const containerWidth = divider.parentElement.getBoundingClientRect().width;

    contentSplitWidth = width_percent * containerWidth;

    // Clamping options width
    if (width_percent * containerWidth < minOptionsWidth) width_percent = (minOptionsWidth / containerWidth);

    if ((1 - width_percent) * containerWidth < minResultsWidth) width_percent = (1 - (minResultsWidth / containerWidth));

    left_panel.style.flex = `0 0 ${width_percent * 100}%`;
    results_container.style.flex = `1`;
}

function setupResultsSplit()
{
    const divider = document.getElementById('results-divider');

    const overlay = document.getElementById("plot-iframe-overlay");

    divider.addEventListener('mousedown', () => {
        isResizingResults = true;
        document.body.style.cursor = 'row-resize';

        overlay.style.pointerEvents = "auto";
    });

    document.addEventListener('mousemove', (e) => {
        if (!isResizingResults) return;

        const containerHeight = divider.parentElement.getBoundingClientRect().height;
        const plotHeight = (e.clientY) / containerHeight;
        console.log(containerHeight);

        resultsSplitSetPercent(plotHeight);
    });

    document.addEventListener('mouseup', () => {
        isResizingResults = false;
        document.body.style.cursor = 'default';

        overlay.style.pointerEvents = "none";
    });

    resultsSplitSetPercent(0.6);
}

function resultsSplitSetPercent(height_percent)
{
    const plot_container = document.getElementById('plot-container');
    const interpretation_container = document.getElementById('interpretation-container');

    const divider = document.getElementById('results-divider');
    const containerHeight = divider.parentElement.getBoundingClientRect().height;

    resultsSplitHeight = height_percent * containerHeight;

    // Clamping height
    if (height_percent * containerHeight < minPlotHeight) height_percent = (minPlotHeight / containerHeight);

    if ((1 - height_percent) * containerHeight < minInterpretationHeight) height_percent = (1 - (minInterpretationHeight / containerHeight));

    plot_container.style.flex = `0 0 ${height_percent * 100}%`;
    interpretation_container.style.flex = `1`;
}


// Option cards

function setupGeneralOptions()
{
    const generalCard = document.getElementById("general-card");

    const experiment_count_input = document.getElementById("experiment_count_input");
    experiment_count_input.addEventListener("change", (event) => {
        inputData.experiment_count = Number(event.currentTarget.value);
        checkInputCorrectness();
    });
    const n_input = document.getElementById("n_input");
    n_input.addEventListener("change", (event) => {
        inputData.n = Number(event.currentTarget.value);
        checkInputCorrectness();
    });
    const m_input = document.getElementById("m_input");
    m_input.addEventListener("change", (event) => {
        inputData.m = Number(event.currentTarget.value);
        checkInputCorrectness();
    });

    const a_min_input = document.getElementById("a_min_input");
    a_min_input.addEventListener("change", (event) => {
        inputData.a_min = Number(event.currentTarget.value);
        checkInputCorrectness();
    });
    const a_max_input = document.getElementById("a_max_input");
    a_max_input.addEventListener("change", (event) => {
        inputData.a_max = Number(event.currentTarget.value);
        checkInputCorrectness();
    });
    const b_min_input = document.getElementById("b_min_input");
    b_min_input.addEventListener("change", (event) => {
        inputData.b_min = Number(event.currentTarget.value);
        checkInputCorrectness();
    });
    const b_max_input = document.getElementById("b_max_input");
    b_max_input.addEventListener("change", (event) => {
        inputData.b_max = Number(event.currentTarget.value);
        checkInputCorrectness();
    });

    const degradation_mode_input = document.getElementById("degradation_mode_input");
    degradation_mode_input.addEventListener("change", (event) => {
        inputData.degradation_mode = event.currentTarget.value;
        checkInputCorrectness();
    });
    const concentrated_range_fraction_input = document.getElementById("concentrated_range_fraction_input");
    concentrated_range_fraction_input.addEventListener("change", (event) => {
        inputData.concentrated_range_fraction = Number(event.currentTarget.value);
        checkInputCorrectness();
    });

    // const use_individual_ranges_input = document.getElementById("use_individual_ranges_input");
    // use_individual_ranges_input.addEventListener("change", (event) => {
    //     inputData.use_individual_ranges = event.currentTarget.checked;
    //     checkInputCorrectness();
    // });
}

function setupAdditionalOptions()
{
    const additionalCard = document.getElementById("additional-card");
    // const showCheckBox = document.getElementById("show-additional-options-checkbox");
    
    // showCheckBox.addEventListener('change', (event) => {
    //     //if (event.currentTarget.checked) additionalCard.style.height = "450px";
    //     //else additionalCard.style.height = "200px";
    // });

    //additionalCard.style.height = "200px";

    const greedy_thrifty_stage_input = document.getElementById("greedy_thrifty_stage_input");
    greedy_thrifty_stage_input.addEventListener("change", (event) => {
        inputData.greedy_thrifty_stage = Number(event.currentTarget.value);
        checkInputCorrectness();
    });
    const thrifty_greedy_stage_input = document.getElementById("thrifty_greedy_stage_input");
    thrifty_greedy_stage_input.addEventListener("change", (event) => {
        inputData.thrifty_greedy_stage = Number(event.currentTarget.value);
        checkInputCorrectness();
    });
    const bkj_stage_input = document.getElementById("bkj_stage_input");
    bkj_stage_input.addEventListener("change", (event) => {
        inputData.bkj_stage = Number(event.currentTarget.value);
        checkInputCorrectness();
    });
    const bkj_rank_input = document.getElementById("bkj_rank_input");
    bkj_rank_input.addEventListener("change", (event) => {
        inputData.bkj_rank = Number(event.currentTarget.value);
        checkInputCorrectness();
    });
    const ctg_stage_input = document.getElementById("ctg_stage_input");
    ctg_stage_input.addEventListener("change", (event) => {
        inputData.ctg_stage_input = Number(event.currentTarget.value);
        checkInputCorrectness();
    });
}

function setupNonOrganicsOptions()
{
    const nonOrganicCard = document.getElementById("non-organic-card");
    const useCheckBox = document.getElementById("use-non-organics-checkbox");
    
    useCheckBox.addEventListener('change', (event) => {
        inputData.use_non_organics = event.currentTarget.checked;
        checkInputCorrectness();
        //if (event.currentTarget.checked) nonOrganicCard.style.height = "450px";
        //else nonOrganicCard.style.height = "200px";
    });

    //nonOrganicCard.style.height = "200px";

    const k_min_input = document.getElementById("k_min_input");
    k_min_input.addEventListener("change", (event) => {
        inputData.k_min = Number(event.currentTarget.value);
        checkInputCorrectness();
    });
    const k_max_input = document.getElementById("k_max_input");
    k_max_input.addEventListener("change", (event) => {
        inputData.k_max = Number(event.currentTarget.value);
        checkInputCorrectness();
    });

    const na_min_input = document.getElementById("na_min_input");
    na_min_input.addEventListener("change", (event) => {
        inputData.na_min = Number(event.currentTarget.value);
        checkInputCorrectness();
    });
    const na_max_input = document.getElementById("na_max_input");
    na_max_input.addEventListener("change", (event) => {
        inputData.na_max = Number(event.currentTarget.value);
        checkInputCorrectness();
    });

    const n_min_input = document.getElementById("n_min_input");
    n_min_input.addEventListener("change", (event) => {
        inputData.n_min = Number(event.currentTarget.value);
        checkInputCorrectness();
    });
    const n_max_input = document.getElementById("n_max_input");
    n_max_input.addEventListener("change", (event) => {
        inputData.n_max = Number(event.currentTarget.value);
        checkInputCorrectness();
    });

    const reduce_min_input = document.getElementById("reduce_min_input");
    reduce_min_input.addEventListener("change", (event) => {
        inputData.reduce_min = Number(event.currentTarget.value);
        checkInputCorrectness();
    });
    const reduce_max_input = document.getElementById("reduce_max_input");
    reduce_max_input.addEventListener("change", (event) => {
        inputData.reduce_max = Number(event.currentTarget.value);
        checkInputCorrectness();
    });
}

function setupRipeningOptions()
{
    const ripeningCard = document.getElementById("ripening-card");
    const useCheckBox = document.getElementById("use-ripening-checkbox");
    
    useCheckBox.addEventListener('change', (event) => {
        inputData.use_ripening = event.currentTarget.checked;
        checkInputCorrectness();
        //if (event.currentTarget.checked) ripeningCard.style.height = "450px";
        //else ripeningCard.style.height = "200px";
    });

    //ripeningCard.style.height = "200px";

    const ripening_stages_input = document.getElementById("ripening_stages_input");
    ripening_stages_input.addEventListener("change", (event) => {
        inputData.ripening_stages = Number(event.currentTarget.value);
        checkInputCorrectness();
    });

    const ripening_min_input = document.getElementById("ripening_min_input");
    ripening_min_input.addEventListener("change", (event) => {
        inputData.ripening_min = Number(event.currentTarget.value);
        checkInputCorrectness();
    });

    const ripening_max_input = document.getElementById("ripening_max_input");
    ripening_max_input.addEventListener("change", (event) => {
        inputData.ripening_max = Number(event.currentTarget.value);
        checkInputCorrectness();
    });
}


function setupButtonsPanel()
{
    const runButton = document.getElementById("run-button");
    runButton.addEventListener("click", () => {
        if (isInputCorrect && !isLoading)
        {
            const loadingImg = document.getElementById("loading-gif");
            loadingImg.style.opacity = "0.5";

            const scaleContainer = document.getElementById("scale-container");
            scaleContainer.style.opacity = "0";

            const plotFrame = document.getElementById("plot-frame");
            plotFrame.style.opacity = "0";

            const text_results_container = document.getElementById("text-results-container");
            text_results_container.style.opacity = "0.0";

            const recommendation_container = document.getElementById("recommendation-container");
            recommendation_container.style.opacity = "0.0";

            setTimeout(() => {
                 window.py.send({ "input_data" : inputData });
            }, 450);
        }
    });

    const ugButton = document.getElementById("ug-button");
    ugButton.addEventListener("click", () => {

        const ug_container = document.getElementById("user-guide-container");

        ug_container.style.visibility = "visible";
        ug_container.style.opacity = "1.0";

        const plot_container = document.getElementById("plot-container");
        plot_container.style.opacity = "0.0";
    });

    const ugCloseButton = document.getElementById("ug-close");
    ugCloseButton.addEventListener("click", () => {

        const ug_container = document.getElementById("user-guide-container");
        ug_container.style.opacity = "0.0";

        const plot_container = document.getElementById("plot-container");
        plot_container.style.opacity = "1.0";

        setTimeout( () => {
            ug_container.style.visibility = "hidden";
        }, 400 );
        
    });
}

function checkInputCorrectness()
{
    isInputCorrect = true;

    const inputs = document.querySelectorAll("[id$='_input']");
    for (let i = 0; i < inputs.length; i++)
    {
        const input = inputs[i];

        const value = parseFloat(input.value);
        const min = parseFloat(input.min);
        const max = parseFloat(input.max);

        if (value < min) 
        {
            input.value = min;
            input.dispatchEvent(new Event("change", { bubbles: true }));
        }

        else if (value > max) 
        {
            input.value = max;
            input.dispatchEvent(new Event("change", { bubbles: true }));
        }
    }

    if (inputData.greedy_thrifty_stage < 2 || inputData.greedy_thrifty_stage > inputData.n / 2)
    {
        isInputCorrect = false;

        const greedy_thrifty_stage_input = document.getElementById("greedy_thrifty_stage_input");
        greedy_thrifty_stage_input.classList.add("wrong");
    }
    else
    {
        const greedy_thrifty_stage_input = document.getElementById("greedy_thrifty_stage_input");
        greedy_thrifty_stage_input.classList.remove("wrong");
    }


    if (inputData.thrifty_greedy_stage < 2 || inputData.thrifty_greedy_stage > inputData.n / 2)
    {
        isInputCorrect = false;

        const thrifty_greedy_stage_input = document.getElementById("thrifty_greedy_stage_input");
        thrifty_greedy_stage_input.classList.add("wrong");
    }
    else
    {
        const thrifty_greedy_stage_input = document.getElementById("thrifty_greedy_stage_input");
        thrifty_greedy_stage_input.classList.remove("wrong");
    }


    if (inputData.bkj_stage < 1 || inputData.bkj_stage > inputData.n)
    {
        isInputCorrect = false;

        const bkj_stage_input = document.getElementById("bkj_stage_input");
        bkj_stage_input.classList.add("wrong");
    }
    else
    {
        const bkj_stage_input = document.getElementById("bkj_stage_input");
        bkj_stage_input.classList.remove("wrong");
    }


    if (inputData.bkj_rank < 1 || inputData.bkj_rank > inputData.n - inputData.bkj_stage + 2)
    {
        isInputCorrect = false;

        const bkj_rank_input = document.getElementById("bkj_rank_input");
        bkj_rank_input.classList.add("wrong");
    }
    else
    {
        const bkj_rank_input = document.getElementById("bkj_rank_input");
        bkj_rank_input.classList.remove("wrong");
    }


    if (inputData.ctg_stage < 2 || inputData.ctg_stage > inputData.n / 2)
    {
        isInputCorrect = false;

        const ctg_stage_input = document.getElementById("ctg_stage_input");
        ctg_stage_input.classList.add("wrong");
    }
    else
    {
        const ctg_stage_input = document.getElementById("ctg_stage_input");
        ctg_stage_input.classList.remove("wrong");
    }

    const runButton = document.getElementById("run-button");
    runButton.disabled = !isInputCorrect;
}


function showResults(results)
{
    // Algorithm Results

    // Clearing old results
    let existing_lines = document.querySelectorAll('.text-result-line');
    for (let i = 0; i < existing_lines.length; i++)
        existing_lines[i].remove();

    let min = 10e10;
    let max = -1;

    for (let i = 0; i < results.statistics_list.length; i++)
    {
        if (results.statistics_list[i][1] < min) min = results.statistics_list[i][1];
        if (results.statistics_list[i][1] > max) max = results.statistics_list[i][1];
    }

    for (let i = 0; i < results.statistics_list.length; i++)
    {
        const algorithm_name = results.statistics_list[i][0];
        const value = results.statistics_list[i][1];

        let line_template = document.getElementById("text-result-entry-template");
        let text_results_container = document.getElementById("text-results-container");

        let clone = line_template.content.cloneNode(true).querySelector(".text-result-line");

        // Customizing message
        let text_result_name = clone.querySelector(".text-result-name");
        let text_result_value = clone.querySelector(".text-result-value");

        const result_number = value * inputData.m;
        const percent_number = (value / max) * 100;

        const result_value_text = result_number.toLocaleString("ru", {
                maximumFractionDigits: 1,
                minimumFractionDigits: 1,
                useGrouping: false
            });

        const percent_text = percent_number.toLocaleString("ru", {
                maximumFractionDigits: 1,
                minimumFractionDigits: 1,
                useGrouping: false
            });

        text_result_name.textContent = String(i) + ". " + algorithm_name;
        text_result_value.textContent = percent_text + "%" + "  :   " + result_value_text + " кг";

        // Appening message
        text_results_container.appendChild(clone);
    }

    // Recommendations
    const recommendation_text = document.getElementById("recommendation-text");
    const rec_algorithm_text = document.getElementById("recommended-algorithm-text");

    rec_algorithm_text.textContent = results.best_strategy;

    const bad_text = document.getElementById("bad-text");
    const bad_algorithm_text = document.getElementById("bad-algorithm-text");

    bad_algorithm_text.textContent = results.worst_strategy;

    // Show scale
    showScale(results.statistics_list);

    // Showing plot
    showPlot();

    const plotFrame = document.getElementById("plot-frame");
    plotFrame.onload = function()
    {
        const loadingImg = document.getElementById("loading-gif");
        loadingImg.style.opacity = "0";

        const scaleContainer = document.getElementById("scale-container");
        scaleContainer.style.opacity = "1.0";

        const plotFrame = document.getElementById("plot-frame");
        plotFrame.style.opacity = "1.0";

        const text_results_container = document.getElementById("text-results-container");
        text_results_container.style.opacity = "1.0";

        const recommendation_container = document.getElementById("recommendation-container");
        recommendation_container.style.opacity = "1.0";

        isLoading = false;
    }
}

async function showPlot() 
{
    const html = await window.backend.loadHtml();
    //document.getElementById("plot").innerHTML = html;

    // const container = document.getElementById("plot");
    // const shadow = container.attachShadow({ mode: "open" });
    // shadow.innerHTML = html;

    const htmlPath = await window.backend.getHtmlPath();
    document.getElementById("plot-frame").src = `file://${htmlPath}`;
}

function showScale(statistics_list)
{
    // Данные об алгоритмах (можно заменить на загрузку из файла)
    // const algorithms = [
    //     { name: "ЖАДНЫЙ", value: 60 },
    //     { name: "БЕРЕЖЛИВЫЙ", value: 20 },
    //     { name: "ВЕНГЕРСКИЙ", value: 100 }
    // ];
    
    const container = document.getElementById('algorithm-markers');
    container.innerHTML = '';

    let min = 10e10;
    let max = -1;

    for (let i = 0; i < statistics_list.length; i++)
    {
        if (statistics_list[i][1] < min) min = statistics_list[i][1];
        if (statistics_list[i][1] > max) max = statistics_list[i][1];
    }
    
    for (let i = 0; i < statistics_list.length; i++)
    {
        const algorithm = statistics_list[i];

        // Ограничиваем значение от 0 до 100
        const value = (algorithm[1] - min) / (max - min);
        
        // Создаем элемент отметки
        const marker = document.createElement('div');
        marker.className = 'scale-marker';
        marker.style.left = `${value * 100}%`;

        marker.innerHTML = `
            <div class="algorithm-name" style="top:${(i % 2) * 50}px">${algorithm[0]}</div>
            <div class="algorithm-value">(${(value * 100).toLocaleString("ru", {    maximumFractionDigits: 0, 
                                                                                    minimumFractionDigits: 0, 
                                                                                    useGrouping: false })}%)</div>
            <div class="marker-dot"></div>
        `;
        
        container.appendChild(marker);
    }
}