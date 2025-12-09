
window.addEventListener("DOMContentLoaded", () => {
    
    window.tabsAPI.onUpdate(({ tabs, active }) => {

        const tabContainer = document.getElementById("tab-container");
        tabContainer.innerHTML = "";

        tabs.forEach((tab, i) => {

            const el = document.createElement("div");
            el.className = "tab";
            el.innerHTML = `
                        <p class="tab-name">Tab ${i + 1}</p>
                        <button class="close-button"></button>`;

            if (i == active)
            {
                el.classList.add("active");
            }

            el.onclick = () => window.tabsAPI.switchTab(i);
            el.querySelector(".close-button").addEventListener("click", (event) => {
                event.stopPropagation();
                window.tabsAPI.closeTab(i);
            });

            tabContainer.appendChild(el);
        });
    });

    const add_button = document.getElementById("add-button");
    add_button.addEventListener("click", () => {
        window.tabsAPI.newTab();
    })
    
    window.tabsAPI.newTab();
});