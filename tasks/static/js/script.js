/*$(document).ready(async function () {
	let response = await fetch("/counter")
	let data = await response.json();
	$("total_task").html(data);
});

$(document).ready(async function() {
	let response_incomplete = await fetch("/incomplete")
	let counter_in = await response_incomplete.json();
	if (counter_in != "0"){
		$("#counter").html("Невыполненных задач: " + counter_in)};
	if (counter_in == "10") {
			$("#too_much").html("Слишком много нерешенных задач!")
		};
});*/

$(document).ready(function () {
	$(document).on('click', '.checkbox', function(){
		

		$(this).parent().addClass('completed');
		$(this).attr('disabled', true);
	
		id = $(this).attr('data-uid');
		$.get("complete/" + id);
		//window.location.reload()
	});

	$(document).on('click', '.remove', function(){
		$(this).parent().remove();
	});
});
