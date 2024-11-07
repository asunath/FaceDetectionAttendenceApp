const form = document.getElementById('leaveForm');
const type = document.getElementById('type')
const startDateInput = document.getElementById('startDate');
const endDateInput = document.getElementById('endDate');


form.addEventListener('submit', function(event) {
    // Parse dates
    const startDate = new Date(startDateInput.value);
    const endDate = new Date(endDateInput.value);
    const differenceInMilliseconds = endDate-startDate;
    const days = differenceInMilliseconds / (1000 * 60 * 60 * 24);
    const selected = document.getElementById('leavetype');
    const option = selected.value;
    // Validate end date
    if (endDate < startDate) {
        event.preventDefault(); // Prevent form submission
        alert('To Date must be after From Date');
    }
    else if (option==='default'){
        event.preventDefault();
        alert("Select a valid leave type!");
    }
    else {
        for (var i = 0; i < data.length; i++) {
            if (option === data[i].leave_type) {
                if (data[i].remaining < days) {
                    event.preventDefault();
                    alert("Don't have enough " + data[i].leave_type + " to Apply");
                }
                else {
                    const dateParts = startDateInput.value.split(' ');
                    const dateString = dateParts.slice(0, 4).join(' ');

                    const endDateParts = endDateInput.value.split(' ');
                    const endDateString = endDateParts.slice(0,4).join(' ');


                    alert('Applied for ' + data[i].leave_type + ' from ' + dateString + ' to ' + endDateString + ' for ' + days + ' days.');
                }
            }
        }
    }
});



