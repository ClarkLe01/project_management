"use strict";
const tags_chart = document.getElementById("kt_project_list_chart").getContext('2d');
const active_num = document.getElementById("num_ActiveProject");
const completed_num = document.getElementById('num_CompletedProject');
const pending_num = document.getElementById('num_PendingProject');
new Chart(tags_chart, {
    type: 'doughnut',
    data: {
        labels:["Active","Completed","Yet to start"],
        datasets: [{
            data:[Number(active_num.innerText),Number(completed_num.innerText),Number(pending_num.innerText)],
            backgroundColor:["#00A3FF","#50CD89","#E4E6EF"],
            hoverOffset: 4,
        }]
    },
    options:{
        chart:{
            fontFamily:"inherit"
        },
        borderWidth:0,
        cutout:"75%",
        cutoutPercentage:65,
        responsive:!0,
        maintainAspectRatio:!1,
        title:{display:!1},
        animation:{
            animateScale:!0,
            animateRotate:!0
        },
        stroke:{
            width:0
        },
        tooltips:{
            enabled:!0,
            intersect:!1,
            mode:"nearest",
            bodySpacing:5,
            yPadding:10,
            xPadding:10,
            caretPadding:0,
            displayColors:!1,
            backgroundColor:"#20D489",
            titleFontColor:"#ffffff",
            cornerRadius:4,
            footerSpacing:0,
            titleSpacing:0
        },
        plugins:{
            legend:{
                display:!1
            }
        }
    }
});

