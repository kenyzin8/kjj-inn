var updateModal = null,
    addModal = null;

$(document).ready(function() {
    setupTableSearch('user-table', 'table-search');
    updateModal = initializeModal("#update-user-modal");
    addModal = initializeModal("#add-user-modal");
});

$(document).on('click', '#add-user-button', function() {
    addModal.show();
});
$(document).on('submit', '#form-add-users', function(e) {
    e.preventDefault();
    var form = $(this);
    var data = form.serialize();
    axios.post(addUserURL, data)
        .then(function (response) {
            
            if(response.data.password_correct === false || response.data.username_exists === true) {
                showError(response.data.message);
                return;
            }

            if(response.data.success === true) {
                const data = response.data.data;

                $(".users-tbody").prepend(`
                    <tr class="bg-white border-b dark:bg-gray-800 dark:border-gray-700 fee-row-${data.id}">
                        <td class="px-6 py-4 whitespace-nowrap">
                            <span class="text-xs font-medium me-2 px-2.5 py-0.5 rounded dark:bg-gray-900 dark:text-[orange] user-index">
                                ${$(".users-tbody tr").length + 1}
                            </span>
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap">
                            <span class="text-xs font-medium me-2 px-2.5 py-0.5 rounded dark:bg-gray-900 dark:text-[orange] user-name">
                                ${data.first_name + " " + data.last_name}
                            </span>
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap">
                            <span class="text-xs font-medium me-2 px-2.5 py-0.5 rounded dark:bg-gray-900 dark:text-[orange] user-username">
                                ${data.username}
                            </span>
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap">
                            <span class="text-xs font-medium me-2 px-2.5 py-0.5 rounded dark:bg-gray-900 dark:text-[orange] user-last-login">
                                N/A
                            </span>
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap">
                            <span class="text-xs font-medium me-2 px-2.5 py-0.5 rounded dark:bg-gray-900 dark:text-[orange] user-date-joined">
                                ${data.date_created}
                            </span>
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap">
                            <span class="text-xs font-medium me-2 px-2.5 py-0.5 rounded dark:bg-gray-900 dark:text-[orange] user-role">
                                ${data.is_staff ? "Admin" : "User"}
                            </span>
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap">
                            <span class="text-xs font-medium me-2 px-2.5 py-0.5 rounded dark:bg-gray-900 dark:text-[orange]">
                                <a class="font-medium text-blue-600 dark:text-[orange] hover:text-[#D18700] cursor-pointer button-update-user" data-user-id="${data.id}">
                                    <i class="fa-solid fa-gear"></i>
                                </a>
                                <a class="font-medium text-blue-600 dark:text-[orange] hover:text-[#D18700] ml-1 cursor-pointer button-delete-user" data-user-id="${data.id}">
                                    <i class="fa-solid fa-trash"></i>
                                </a>
                            </span>
                        </td>
                    </tr>
                `);

                closeModals();
                showSuccess(response.data.message);
            }
            else{
                closeModals();
                showError(response.data.message);
            }
        })
        .catch(function (error) {
            showError(error.message);
        })
});

$(document).on('click', '.button-update-user', function() {
    var userId = $(this).data('user-id');
    var firstName = $(this).data('user-first-name');
    var lastName = $(this).data('user-last-name');
    var username = $(this).data('user-username');
    var isStaff = $(this).data('user-is-staff');

    $("#user-id-update").val(userId);
    $("#firstname-update").val(firstName);
    $("#lastname-update").val(lastName);
    $("#username-update").val(username);
    $("#is-staff-update").prop('checked', isStaff === "True" ? true : false);

    updateModal.show();
});
$(document).on('submit', '#form-update-users', function(e) {
    e.preventDefault();
    var form = $(this);
    var data = form.serialize();
    axios.post(updateUserURL, data)
        .then(function (response) {

            if(response.data.password_correct === false || response.data.username_exists === true) {
                showError(response.data.message);
                return;
            }

            if(response.data.success === true) {
                const data = response.data.data;
                var row = $(`.user-row-${data.id}`);
                row.find('.user-name').text(data.first_name + " " + data.last_name);
                row.find('.user-username').text(data.username);
                row.find('.user-role').text(data.is_staff ? "Admin" : "User");

                closeModals();
                showSuccess(response.data.message);
            }
            else{
                closeModals();
                showError(response.data.message);
            }
        })
        .catch(function (error) {
            showError(error.message);
        })
});

$(document).on('click', '.button-delete-user', function() {
    var userId = $(this).data('user-id');
    var row = $(`.user-row-${userId}`);
    var firstName = $(this).data('user-first-name');
    var lastName = $(this).data('user-last-name');
    var username = $(this).data('user-username');
    var isStaff = $(this).data('user-is-staff');

    Swal.fire({
        title: "Confirmation",
        html: `<span class="font-semibold text-md">Are you sure you want to delete ${firstName} ${lastName} (${username})?</span>`,
        icon: "warning",
        showDenyButton: true,
        confirmButtonColor: "orange",
        denyButtonColor: "#232323",
        confirmButtonText: "Yes",
        denyButtonText: `No`,
        allowOutsideClick: false,
        animation: true
        }).then((result) => {
        if (result.isConfirmed) {
            axios.post(deleteUserURL, {id: userId},
                {headers: {'X-CSRFToken': getCSRFTokenFromCookies()}})
                .then(function (response) {
                    if(response.data.success === true) {
                        row.remove();
                        showSuccess(response.data.message);
                    }
                    else{
                        showError(response.data.message);
                    }
                })
                .catch(function (error) {
                    showError(error.message);
                })
        }
    });

});