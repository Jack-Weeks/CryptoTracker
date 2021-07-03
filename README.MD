<html>
    <head>
        <title>Convert JSON Data to HTML Table</title>
        <style>
            th, td, p, input {
                font:14px Verdana;
            }
            table, th, td 
            {
                border: solid 1px #DDD;
                border-collapse: collapse;
                padding: 2px 3px;
                text-align: center;
            }
            th {
                font-weight:bold;
            }
        </style>
    </head>
    <body>
        <input type="button" onclick="CreateTableFromJSON()" value="Create Table From JSON" />
        <p id="showData"></p>
    </body>
    
    <script>
        function CreateTableFromJSON() {
            var myBooks = [{'XCH': {'Current Price': 299.1599659171429, 'Current Balance': 0.166151507937, 'Average_Hourly_Increase': 0.0, 'Average_Hourly_Value_Increase': 0.0, 'Average_Daily_Increase': 0.0, 'Average_Daily_Value_Increase': 0.0, 'Average_Weekly_Increase': 0.0, 'Average_Weekly_Value_Increase': 0.0, 'Average_Monthly_Increase': 0.0, 'Average_Monthly_Value_Increase': 0.0}, 'XFX': {'Current Price': 0, 'Current Balance': 3.385552904469, 'Average_Hourly_Increase': 0.0009777605681073253, 'Average_Hourly_Value_Increase': 0.0, 'Average_Daily_Increase': 0.00069432657406668, 'Average_Daily_Value_Increase': 0.0, 'Average_Weekly_Increase': 0.00069432657406668, 'Average_Weekly_Value_Increase': 0.0, 'Average_Monthly_Increase': 0.00069432657406668, 'Average_Monthly_Value_Increase': 0.0}, 'CGN': {'Current Price': 0, 'Current Balance': 5500.0, 'Average_Hourly_Increase': 22.727272727272727, 'Average_Hourly_Value_Increase': 0.0, 'Average_Daily_Increase': 41.666666666666664, 'Average_Daily_Value_Increase': 0.0, 'Average_Weekly_Increase': 41.666666666666664, 'Average_Weekly_Value_Increase': 0.0, 'Average_Monthly_Increase': 41.666666666666664, 'Average_Monthly_Value_Increase': 0.0}, 'SPARE': {'Current Price': 0, 'Current Balance': 24.0, 'Average_Hourly_Increase': 0.0, 'Average_Hourly_Value_Increase': 0.0, 'Average_Daily_Increase': 0.0, 'Average_Daily_Value_Increase': 0.0, 'Average_Weekly_Increase': 0.0, 'Average_Weekly_Value_Increase': 0.0, 'Average_Monthly_Increase': 0.0, 'Average_Monthly_Value_Increase': 0.0}, 'AR': {'Current Price': 10.60167500061067, 'Current Balance': 0.05, 'Average_Hourly_Increase': 0.0, 'Average_Hourly_Value_Increase': 0.0, 'Average_Daily_Increase': 0.0, 'Average_Daily_Value_Increase': 0.0, 'Average_Weekly_Increase': 0.0, 'Average_Weekly_Value_Increase': 0.0, 'Average_Monthly_Increase': 0.0, 'Average_Monthly_Value_Increase': 0.0}}"
            ]
    
            // EXTRACT VALUE FOR HTML HEADER. 
            // ('Book ID', 'Book Name', 'Category' and 'Price')
            var col = [];
            for (var i = 0; i < myBooks.length; i++) {
                for (var key in myBooks[i]) {
                    if (col.indexOf(key) === -1) {
                        col.push(key);
                    }
                }
            }
    
            // CREATE DYNAMIC TABLE.
            var table = document.createElement("table");
    
            // CREATE HTML TABLE HEADER ROW USING THE EXTRACTED HEADERS ABOVE.
    
            var tr = table.insertRow(-1);                   // TABLE ROW.
    
            for (var i = 0; i < col.length; i++) {
                var th = document.createElement("th");      // TABLE HEADER.
                th.innerHTML = col[i];
                tr.appendChild(th);
            }
    
            // ADD JSON DATA TO THE TABLE AS ROWS.
            for (var i = 0; i < myBooks.length; i++) {
    
                tr = table.insertRow(-1);
    
                for (var j = 0; j < col.length; j++) {
                    var tabCell = tr.insertCell(-1);
                    tabCell.innerHTML = myBooks[i][col[j]];
                }
            }
    
            // FINALLY ADD THE NEWLY CREATED TABLE WITH JSON DATA TO A CONTAINER.
            var divContainer = document.getElementById("showData");
            divContainer.innerHTML = "";
            divContainer.appendChild(table);
        }
    </script>
    </html>