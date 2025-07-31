
const MONTHS = ["January","February","March","April","May","June","July","August","September","October","November","December"];

function current_month_name() {
    const d = new Date();
    return MONTHS[d.getMonth()];
}
