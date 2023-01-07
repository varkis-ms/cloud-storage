var cnt = 0;

function onClockButton(cnt_click) {
    cnt++;
    cnt_click.innerHTML = "Cnt = " + cnt;
    console.log(cnt_click);
}