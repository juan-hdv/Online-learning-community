// var csrftoken = "";

/** General use functions 
 */ 

/** key Events
*/
function keyEvents (event) {
  if (event.keyCode === 13) {
    // Cancel the default action, if needed
    event.preventDefault();
    // Trigger the corresponding button element (event.currentTarget.selectorParam) with a click
    document.getElementById(event.currentTarget.selectorParam).click();
  }
} // End keyEvents

/** SET Intersection
	Return the intersection between 2 sets
 */
function setIntersection(set1, set2) {
	return new Set(Array.from(set1).filter(x => set2.has(x)))
}
/** END General use functions  
 */

/** GetCheckedCategoriesList
    @Returns Set of all of the checked categories in the checkbox list of courseCategories
    		 except the "ALL" Category.
 */
 function GetCheckedCategoriesSet () {
 	// Make a SET of checked values (categories), except "ALL"
	var filterCategories = new Set();
	var checkboxes = document.querySelectorAll("input[name='courseCategories']:checked")
	for (var i = 0; i < checkboxes.length; i++)
		filterCategories.add(checkboxes[i].value);
	return filterCategories;
} // END GetCheckedCategoriesSet

/** GetCourseCategoriesSet
    @Returns Set of all of the course categories.
 */
function GetCourseCategoriesSet(courseObject) {
	let courseCategorySet = new Set (courseObject.getAttribute('data-categories').replace(/[\[|\]]/g,"").split(","));
	return courseCategorySet;
} // GetCourseCategoriesSet

/** Filter the list of courses by category
	@category - Clicked categoty
 */
 function filterCoursesByCategory(category) {
	// Get category id clicked element
	var id = category.getAttribute('data-categoryid');
 	// Manage clicked checkboxes according to "All Courses" (id === '0')
 	var checkboxes = document.querySelectorAll("input[name='courseCategories']");
 	if (id === '0') {
 		let checked = category.checked;
 		// Update all checkboxes according to All Categories id === '0'
		for (var i = 1; i < checkboxes.length; i++)
			checkboxes[i].checked = checked;
 	} else {
		if (!category.checked)
	 		// If any of the other checboxes is uncheked, "ALL Categories" (Categories id === '0') must be uncheked 
			checkboxes[0].checked = false;
		else {
			// If all the categories, except 0, are checked, ALL must be checked
			let count = 0;
			for (var i = 1; i < checkboxes.length; i++)
				if (checkboxes[i].checked)
					count++;
			if (count == checkboxes.length-1)
				checkboxes[0].checked = true;
		}
 	}
 	// Make a SET of checked values (categories), except "ALL"
	var filterCategories = GetCheckedCategoriesSet();
	// Set visible only courses with
	document.querySelectorAll('[data-selector="course-entry"]').forEach ( course => {
		if (id==0) 
			if (category.checked)
			// Show courses for "All Categories" => ALL				
				course.classList.remove("d-none");
			else
				course.classList.add("d-none");
		else { // Show courses for a specific set of selected categories
			let courseCategorySet = GetCourseCategoriesSet(course);
			// If there is an intersection between course categories and selected categories, they must be displayed
			let canditateCourse = (setIntersection(courseCategorySet, filterCategories).size > 0);
			if (canditateCourse)
				course.classList.remove("d-none"); // Unhidde
			else
				course.classList.add("d-none"); // Hide
		}
	}); 
} // End filterCoursesByCategory

/** Filter the courses according to a filter string. The filter must apply over the category filter previously applied.
	@filterstring - Words list to find in the course list.
 */
function filterCoursesByString(filterstring) {
 	// Make a SET of checked values (categories), except "ALL"
	var filterCategories = GetCheckedCategoriesSet();	
	// Set visible only courses filtered
	document.querySelectorAll('[data-selector="course-entry"]').forEach ( course => {
		// Get the Course Categories
		var courseCategorySet = GetCourseCategoriesSet(course);
		// If the is an intersection between the Course categories and selected categories, This is a candidate Course
		var candidateCourse = (setIntersection(courseCategorySet, filterCategories).size > 0);
		if (!filterstring) { // All courses for Selected Categories must shown
			// If there is an intersection between course categories and selected categories, the course must be displayed
			if (candidateCourse)
				course.classList.remove("d-none"); // Unhidde
			else
				course.classList.add("d-none"); // Hide
		} else { // The courses for teh selected categories must be filtered according to the filterstring
			if (candidateCourse) {
				// Get the complete contents of a course descriptión: NAME + DESCRIPTION
				let content = course.getAttribute('data-content');
				// Sanitize search string and split
				let wordslist = filterstring.replace(/\[\],\.#\$%&\/\\@~!\?¿-_\+\^\*{}\|]/g,"").split (" ");
				let matchedwords = wordslist.filter(word => content.includes(word));
				// If any word is a substring of the content of the Course, I must be displayed
				if (matchedwords && matchedwords.length > 0)
					course.classList.remove("d-none"); // Unhidde
				else
					course.classList.add("d-none"); // Hidde
			}
		}
	}); 
} // filterCoursesByString

function getAddsInfo (courseid) {
	// Get complete adds list for course
	let addsList = document.querySelectorAll('input'+`.check-${courseid}`+'[type="checkbox"]');
	/* Get number of selected (checked) course adds (all checked -checkboxes- of a given class)
	   And calculate price */
	var freeAdds = 0; // Num if free adss
	var extrapriceAdds = 0;
	addsList.forEach( add => { 
		if (add.checked) {
			if (add.getAttribute('data-free').toLowerCase() == 'true')
				freeAdds++;
			else
				extrapriceAdds += parseFloat(add.getAttribute('data-extraprice'));
		}
	});
	response = {"list": addsList, 
				"numberfree": freeAdds, 
				"extraprice": extrapriceAdds }
	return response;
} // End getAddsInfo

function updateOrderCoursePrice (courseid) {
    let cprice = parseFloat(document.querySelector(`#modal-${courseid}-coursePrice`).getAttribute('value'));
	let adds = getAddsInfo (courseid); // Get adds complete info, including total extraprices 
    totalPrice = cprice + adds.extraprice;
    document.querySelector(`#modal-${courseid}-coursePrice`).innerHTML = totalPrice.toFixed(2);
    return adds;
} // End updateOrderCoursePrice

/** EVENT HANDLER - When selected course Adds check
	Control number of free adds and calculate price
	@add - checked add
*/
function checkOrderAdds (courseid) {
	// Get max number of free adds allowed
	let maxAdds = document.querySelector(`#modal-${courseid}-courseAdds`).getAttribute('value');

	// Update course price and get adds list, and num of free adds selected
	let adds = updateOrderCoursePrice (courseid);
	let addsList = adds.list;
	let numAdds = adds.numberfree;
	
	// Update nmumber of free adds available to select
	document.querySelector(`#modal-${courseid}-courseAdds`).innerHTML = `${maxAdds-numAdds}`;

	if (numAdds == maxAdds) { // Disable rest of free adds checkboxes
		addsList.forEach ( add => {	
			if (!add.checked && add.getAttribute('data-free').toLowerCase() == 'true')
				add.disabled = true; 
		}); 
	} else if (numAdds < maxAdds) { // Enable all disabled items
		addsList.forEach ( add => {	if (add.disabled) add.disabled = false; }); 
	}
} // End checkOrderAdds

/** When load page */
document.addEventListener('DOMContentLoaded', load);
/** Load
 * - Set "onclick" event handlers for ...
 * - Set "change"  event handlers for ...
 */
function load () {
	/** Click event handler for click card-link Category link
	  */
	document.querySelectorAll("input[name='courseCategories']").forEach ( category => {
		category.addEventListener('click', event => { 
			filterCoursesByCategory(category) 
		});
	}); // End .plusButton'.onclick

	/** Click event handler for button search (filter)
      */
	document.querySelectorAll("input[name='courseAdds']").forEach ( add => {
		add.addEventListener('change', event => { 
			checkOrderAdds(add.getAttribute('data-courseid'));// Check adds for course
		});
	}); // End course Adds Changes

	/** Click event handler for filter by string click or <Enter> Key
 	*/
	var stringInputField = document.querySelector("#filterString");
	if (typeof stringInputField !== 'undefined' && stringInputField != null) {
		// Add a key event to input field
	    stringInputField.addEventListener("keyup", keyEvents, false);
	    stringInputField.selectorParam = 'filterButton';
	    // Click event for button
		document.querySelector("#filterButton").addEventListener('click', event => {
	  		filterCoursesByString(stringInputField.value);
		}); // End #filterButton

		/** Click event handler for clear filter by string
	 	*/
		document.querySelector("#clearButton").addEventListener('click', event => {
			stringInputField.value='';
	  		filterCoursesByString("");
		}); // End #filterButton
	}

	/** RATINGS **/
	function setRatingStar(starRating) {
		starRating.forEach ( item => {
			if (parseInt(item.parentNode.querySelector('input#userrating').value) >= parseInt(item.getAttribute('data-rating')))
			  item.classList.add('checked');
			else
			  item.classList.remove('checked');
		});
	} // End setRatingStar

	/**	Select Rating
	 */
	document.querySelectorAll (".starsBox > i").forEach ( item => {
		item.addEventListener('click', event => {
			item.parentNode.querySelector('input#userrating').value = item.getAttribute('data-rating');
			// Set rating 
			setRatingStar(item.parentNode.querySelectorAll (".starsBox > i"));
		}); // End click starsBox>i
	});

	/**	Clear Rating
	 */
	document.querySelectorAll('.starsBox > button#clear').forEach ( item => {
		item.addEventListener('click', event => {
			item.parentNode.querySelector('input#userrating').value = 0;
		  	item.parentNode.querySelectorAll (".starsBox > i").forEach ( item => {
				item.classList.remove('checked');
			});
		}); // End click starsBox>i
    });
	// Update all stars
	setRatingStar(document.querySelectorAll (".starsBox > i"));

	// csrftoken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
} // End load
