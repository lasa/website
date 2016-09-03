window.onload = function () {
		// Any of the following formats may be used
		var ctx = document.getElementById("myChart");
		var myChart = new Chart(ctx, {
		type: 'pie',
		data: {
			labels: ["Black/African American", "American Indian/Alaska Native","Asian","Native Hawaiian/Other Pacific Islander","Hispanic","Multi-Racial","White"],
			datasets: [{
				label: 'Racial Makeup',
				data: [1.6,0.1,20,0.4,17.4,4.8,55.7],
				backgroundColor: [
					'rgba(255, 99, 132, 0.2)',
					'rgba(255, 176, 197, 0.2)',
					'rgba(255, 255, 97, 0.2)',
					'rgba(97, 255, 97, 0.2)',
					'rgba(97, 176, 255, 0.2)',
					'rgba(136, 97, 255, 0.2)',
					'rgba(176, 97, 255, 0.2)',
				],
				borderColor: [
					'rgba(255, 99, 132, 1)',
					'rgba(255, 176, 197, 1)',
					'rgba(255, 255, 97, 1)',
					'rgba(97, 255, 97, 1)',
					'rgba(97, 176, 255, 1)',
					'rgba(136, 97, 255, 1)',
					'rgba(176, 97, 255, 1)',
				],
				borderWidth: 1.5
			}]
		},
		options: {
			scales: {
				
			}
		}
	});
}