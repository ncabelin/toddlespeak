$(function() {
	// click event handler for Tabs (Add word, Add goal)
	$('#myTabs a').click(function(e) {
		e.preventDefault();
		$(this).tab('show');
	});

	// show default tab 'Add Word'
	$('#myTabs a[href="#wordPanel"]').tab('show');

	// returns date only in m d, y format
	function filterDate(dateStr) {
		var arr = dateStr.split(' ');
		return arr[2] + ' ' + arr[1] + ', ' + arr[3];
	};

	// add word modal
	$('#addWordBtn').click(function() {
		// empty modal title, body, submit button
		$('#wordForm, #goalForm').remove();
		var addWordForm = $('<form />', { action: '/addword', method: 'POST', class: 'form-box', id: 'wordForm'}),
			formGroup = $('<div />', { class: 'form-group' }),
			wordField = $('<input />', { class: 'form-control', type: 'text', name: 'word',
						id: 'wordInput', placeholder: 'word'}),
			soundField = $('<input />', { class: 'form-control', type: 'text', name: 'sound',
						id: 'soundInput', placeholder: 'sound'})
			textField = $('<textarea />', { class: 'form-control', name: 'description',
						id: 'soundInput', placeholder: 'description'}),
			submitForm = $('<input />', { type: 'submit', class: 'hidden', id: 'addWordSubmitBtn'}),
			submitModal = $('<label />', { for: 'addWordSubmitBtn', class: 'btn btn-primary', text: 'Save'});
		// populate modal form
		addWordForm.append(formGroup, wordField, soundField, textField, submitForm)
		$('#modalTitle').html('Add Word');
		$('#modalBody').append(addWordForm);
		$('#submitBtn').html(submitModal);
		// open modal
		$('#showModal').trigger('click');
		$('#wordForm').submit(function(e) {
			e.preventDefault();
			// check if word and sound fields are empty
			var word = $('#wordInput').val(),
					sound = $('#soundInput').val();
			if (!(word && sound)) {
				console.log('error');
				$('#errMsg').html('<div class="alert alert-danger">Fill up all fields</div>');
				return
			}
			$.ajax({
				url: '/addword',
				method: 'POST',
				data: $('#wordForm').serialize(),
				dataType: 'json'
			}).done(function(result) {
				$('.close').trigger('click');
				console.log('Saved Word');
				getWords();
			}).fail(function(e) {
				console.log(e);
			});
		});
	});

	$('#addGoalBtn').click(function(e) {
		// empty modal title, body, submit button
		$('#wordForm, #goalForm').remove();
		var addGoalForm = $('<form />', { action: '/addgoal', method: 'POST', class: 'form-box', id: 'goalForm'}),
			formGroup = $('<div />', { class: 'form-group' }),
			goalField = $('<input />', { class: 'form-control', type: 'text', name: 'goal',
						id: 'goalInput', placeholder: 'word'}),
			textField = $('<textarea />', { class: 'form-control', name: 'description',
						id: 'descGoalInput', placeholder: 'description'}),
			submitForm = $('<input />', { type: 'submit', class: 'hidden', id: 'addGoalSubmitBtn'}),
			submitModal = $('<label />', { for: 'addGoalSubmitBtn', class: 'btn btn-primary', text: 'Save'});
		// populate modal form
		addGoalForm.append(formGroup, goalField, textField, submitForm)
		$('#modalTitle').html('Add Goal');
		$('#modalBody').append(addGoalForm);
		$('#submitBtn').html(submitModal);
		// open modal
		$('#showModal').trigger('click');
		$('#goalForm').submit(function(e) {
			e.preventDefault();
			// check all fields
			var goal = $('#goalInput').val(),
					desc = $('#descGoalInput').val();
			if (!goal) {
				$('#errMsg').html('<div class="alert alert-danger">Fill up all fields</div>');
				return
			}
			var data = $('#goalForm').serialize();
			console.log(data);
			$.ajax({
				url: '/addgoal',
				method: 'POST',
				data: { goal: goal, description: desc },
				dataType: 'json'
			}).done(function(result) {
				$('.close').trigger('click');
				console.log('Saved Goal');
				getGoals();
			}).fail(function(e) {
				console.log(e)
			});
		});
	});

	var addGoalForm = $('<form />', { action: '/addgoal', method: 'POST'})

	var getWords = function() {
		$.ajax({
			url: '/getwords',
			method: 'GET',
			dataType: 'json'
		}).done(function(result) {
			console.log(result);
			var words = result.Words;
			$('#wordList').empty();
			words.forEach(function(w) {
				$('#wordList').append('<tr class="word-row" data-id="' + w.word_id + '"><td class="word">' + w.word + '</td><td class="sound">' + 
					w.sound + '</td><td class="description">'+ w.description + '</td><td class="hidden">' + w.word_id + '</td><td>' + filterDate(w.date_heard)
					+ '</td></tr>');
			})
			$('#wordSum').text(words.length);
			$('.word-row').click(function(e) {
				var row = this.getElementsByTagName('td');
				var editWordForm = $('<form />', { action: '/editword', method: 'POST', class: 'form-box' }),
						formGroup = $('<div />', { class: 'form-group' }),
						idField = $('<input />', { class: 'hidden', name: 'id', value: row[3].innerText }),
						wordField = $('<input />', { class: 'form-control', type: 'text', name: 'word',
								id: 'wordInput', placeholder: 'word', value: row[0].innerText }),
						soundField = $('<input />', { class: 'form-control', type: 'text', name: 'sound',
								id: 'soundInput', placeholder: 'sound', value: row[1].innerText })
						textField = $('<textarea />', { class: 'form-control', name: 'description',
								id: 'soundInput', placeholder: 'description', value: row[2].innerText }),
						submitForm = $('<input />', { type: 'submit', class: 'hidden', id: 'editWordSubmitBtn'}),
						submitModal = $('<label />', { for: 'editWordSubmitBtn', class: 'btn btn-primary', text: 'Save'});
						editWordForm.append(formGroup, wordField, soundField, textField, submitForm);

				$('#modalTitle').html('Edit Word');
				$('#modalBody').append(editWordForm);
				$('#submitBtn').html(submitModal);
				// open modal
				$('#showModal').trigger('click');
			})
		}).fail(function(e) {
			console.log(e);
		});
	}

	getWords();

	var getGoals = function() {
		$.ajax({
			url: '/getgoals',
			method: 'GET',
			dataType: 'json'
		}).done(function(result) {
			console.log(result);
			var goals = result.Goals;
			$('#goalList').empty();
			goals.forEach(function(g) {
				$('#goalList').append('<li>' + g.goal +'</li>');
			})
			$('#goalSum').text(goals.length);
		}).fail(function(e) {
			console.log(e);
		});
	}

	getGoals();

});