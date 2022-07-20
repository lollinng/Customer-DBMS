console.log("hi");
$(document).ready(function () {
	console.log("clicker");
	$(".jq")
		.unbind("click")
		.bind("click", function (e) {
			var rowCount = $("#myTable tr").length;
			console.log(rowCount);
			if (rowCount <= 1) {
				console.log("clicker button");
				console.log($(".search").val());
				$.ajax({
					url: "../product_list",
					type: "get",
					contentType: "application/json",
					data: {
						button_text: $(".search").val(),
					},
					success: function (response) {
						var table = document.getElementById("myTable");
						console.log(response.data);
						query = response.data;
						console.log(query.length);
						for (let i = 0; i < query.length; i++) {
							var row = table.insertRow(i + 1);
							var cell1 = row.insertCell(0);
							var cell2 = row.insertCell(1);
							var cell3 = row.insertCell(2);
							var cell4 = row.insertCell(3);
							var cell5 = row.insertCell(4);

							cell1.innerHTML = query[i]["name"];
							cell2.innerHTML = query[i]["email"];
							cell3.innerHTML = query[i]["phone"];
							cell4.innerHTML = query[i]["no_products"];
							cell5.innerHTML = query[i]["shopping_value"];
						}
					},
				});
			}
		});
});
