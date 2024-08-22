
function yaml2html() {

    let jsonObj = JSON.parse(jsonData);
    let table =  `<table>
        ${convert(jsonObj, "")}
    </table>`;

    console.log(table)
    document.getElementById("my-table").innerHTML = table
}

function convert(item, body) {
    if (item instanceof Array) {
        let itemVal = item[0];

        // If the value is an object
        if (itemVal instanceof Object) {
            body = createlistTable(item, body);
        } else {
            // If the value is a string element
            for (let idx in item) {
                body += "<li>" + item[idx] + "</li>";
            }
        }
    } else {
        for (let itemKey in item) {
            let itemVal = item[itemKey];

            // If the value is an object
            if (itemVal instanceof Object) {
                body += "<tr><th>" + itemKey + "</th>";
                body += "<td><table>";
                body = convert(itemVal, body);
                body += "</table></td></tr>";

            } else {
                // If the value is a string element
                body += "<tr><th>" + itemKey + "</th>";
                body += "<td>" + itemVal + "</td></tr>";
            }
        }
    }

    return body;
}

// For a List of Hash, create a table
function createlistTable(item, body) {

    // Create a list of unique keys
    var childKeyList = new Array();
    for (let idx in item) {

        let itemVal = item[idx];
        let child = itemVal;

        for (let childKey in child) {
            if (childKeyList.indexOf(childKey) == -1) {
                childKeyList.push(childKey);
            }
        }
    }

    body += "<table><tr>";

    // Table Header
    for (let idx in childKeyList) {
        body += "<th>" + childKeyList[idx] + "</th>";
    }

    body += "</tr>";

    // Table Data Section
    for (let idx in item) {

        let childHash = item[idx];
        body += "<tr>";

        for (let idx in childKeyList) {

            let childVal = childHash[childKeyList[idx]];

            // Recursive call if child hierarchy is an object
            if (childVal instanceof Object) {
                body += "<td>";
                body += "<table>";
                body = convert(childVal, body);
                body += "</table></td>";
            } else {

                body += "<td>" + childVal + "</td>";
            }
        }
        body += "</tr>";

    }

    return body;
}