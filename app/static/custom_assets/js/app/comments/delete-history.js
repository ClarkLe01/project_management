function removeAllHistory() {
    let parent = document.getElementById("kt_histories");
    let histories = parent.querySelectorAll('.history-object');
    histories.forEach(history => history.remove());
}