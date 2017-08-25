$(document).ready(function(){
	$('th').click(function(){
		var column = $(this).attr('class')
		var table = document.getElementById('results_table')
		var switching = true;
		var dir = 'asc';
		var switch_count = 0;
		while (switching){
			switching = false;
			var rows = table.getElementsByTagName('tr');
			for (var i=1; i < (rows.length - 1); i++){
				var shouldSwitch = false;
				var this_cell = rows[i].getElementsByClassName(column)[0];
				var next_cell = rows[i + 1].getElementsByClassName(column)[0];
				console.log(this_cell.textContent)
				if (dir == 'asc'){
					if (this_cell.textContent.toLowerCase() > next_cell.textContent.toLowerCase()){
						shouldSwitch = true;
						break;
					}
				}
				else if (dir == "desc"){
					if (this_cell.textContent.toLowerCase() < next_cell.textContent.toLowerCase()){
						shouldSwitch = true;
						break;
					}
				}
			}
			if (shouldSwitch){
				rows[i].parentNode.insertBefore(rows[i+1], rows[i]);
				switching = true;
				switch_count ++;
			}
			else {
				if (switch_count === 0 && dir === 'asc'){
					dir = 'desc';
					switching = true;
				}
			}
		}
	})
})