function openPopup(userId){

    var url = "/api/userLeaveHistory/" + userId + "/";
    fetch(url)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            buildTable(data.user_history);
            detailsTable(data.leave_available);
        })
        .catch(error => {
            console.error('Error:', error);
        });

    document.getElementById('details').style.filter = 'blur(5px)';
    document.getElementById('popup_window').style.display = 'block';
}



function closePopup(){
    document.getElementById('popup_window').style.display = 'none';
    document.getElementById('details').style.filter = 'none';
}




function detailsTable(data) {
    var table = document.getElementById('details_table');
    table.innerHTML = '';
    

    var count = data.length;
    console.log(count);

    // var row = table.insertRow();
    // var cell = row.insertCell();
    // cell.textContent = '';
    // for (var i = 0; i < count; i++) {
    //     var cell = row.insertCell();
    //     cell.textContent = data[i].leave_type;
    // }

    // var row = table.insertRow();
    // var cell = row.insertCell();
    // cell.textContent = 'Allowed';
    // for (var i = 0; i < count; i++) {
    //     var cell = row.insertCell();
    //     cell.textContent = data[i].limit;
    // }

    // var row = table.insertRow();
    // var cell = row.insertCell();
    // cell.textContent = 'Remaining';
    // for (var i = 0; i < count; i++) {
    //     var cell = row.insertCell();
    //     cell.textContent = data[i].remaining;
    // }


    var transposedData = [[''], ['Allowed'], ['Remaining']];
    for (var i = 0; i < data.length; i++) {
        transposedData[0].push(data[i].leave_type);
        transposedData[1].push(data[i].limit);
        transposedData[2].push(data[i].remaining);
    }

    // Insert data into the table column-wise
    for (var i = 0; i < transposedData.length; i++) {
        var row = table.insertRow();
        for (var j = 0; j < transposedData[i].length; j++) {
            var cell = row.insertCell();
            cell.textContent = transposedData[i][j];
        }
    }


    table.rows[0].classList.add('headings');

    // Add CSS class to the first cell of each row
    for (var i = 0; i < table.rows.length; i++) {
        table.rows[i].cells[0].classList.add('headings');
    }
}



function buildTable(data) {
    var table = document.getElementById('history_table');
    // To empty the table content
    table.innerHTML = '';

    // Add headers
    var headers = ['SL.No', 'Type', 'Starting Date', 'Ending Date', 'Status'];
    var headerRow = table.insertRow();
    headers.forEach(function(headerText) {
        var th = document.createElement('th');
        th.textContent = headerText;
        headerRow.appendChild(th);
    });

    // Add data
    var index = 0;
    data.forEach(function(item) {
        if (item.status != "Submitted") {
            var row = table.insertRow();

            var slNoCell = row.insertCell();
            slNoCell.textContent = index + 1;
    
            var typeCell = row.insertCell();
            typeCell.textContent = item.type;
    
            var startDateCell = row.insertCell();
            startDateCell.textContent = item.startDate;
    
            var endDateCell = row.insertCell();
            endDateCell.textContent = item.endDate;
    
            var statusCell = row.insertCell();
            statusCell.textContent = item.status;

            index += 1;
        }
    });

    // Display's message if there is no data to be shown
    if (!index) {
        var messageRow = table.insertRow();
        var messageCell = messageRow.insertCell();
        messageCell.textContent = "No Leave History Found";
        messageCell.colSpan = 5;
    }
    // console.log(data.length);
}