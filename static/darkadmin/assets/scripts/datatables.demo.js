/**
 * Theme: Ninja Admin Template
 * Author: NinjaTeam
 * Module/App: Data Tables
 */

(function ($) {
    "use strict";

    if ($('#example').length)
        $('#example').DataTable();

    if ($('#repairstable').length)
        $('#repairstable').DataTable({
            "order": [[2, 'desc']],
        });

    if ($('#example2').length)
        $('#example2').DataTable({
            "pageLength": 50
        });
    if ($('#example1234').length)
        $('#example1234').DataTable({
            "pageLength": 50
        });
    if ($('#example12345').length)
        $('#example12345').DataTable({
            "pageLength": 50
        });

    if ($('#example-scroll-y').length)
        $('#example-scroll-y').DataTable({
            "scrollY": "200px",
            "scrollCollapse": true,
            "paging": false
        });

    if ($('#example-scroll-y-2').length)
        $('#example-scroll-y-2').DataTable({
            "scrollY": "200px",
            "scrollCollapse": true,
            "paging": false
        });

    if ($('#example-row-grouping').length) {
        var table = $('#example-row-grouping').DataTable({
            "columnDefs": [
                {"visible": false, "targets": 2}
            ],
            "order": [[2, 'asc']],
            "displayLength": 100,
            "drawCallback": function (settings) {
                var api = this.api();
                var rows = api.rows({page: 'current'}).nodes();
                var last = null;

                api.column(2, {page: 'current'}).data().each(function (group, i) {
                    if (last !== group) {
                        $(rows).eq(i).before(
                            '<tr class="group"><td colspan="5">' + group + '</td></tr>'
                        );

                        last = group;
                    }
                });
            }
        });

        // Order by the grouping
        $('#example-row-grouping tbody').on('click', 'tr.group', function () {
            var currentOrder = table.order()[0];
            if (currentOrder[0] === 2 && currentOrder[1] === 'asc') {
                table.order([2, 'desc']).draw();
            } else {
                table.order([2, 'asc']).draw();
            }
            return false;
        });
    }

    if ($('#example-row-grouping-viplati').length) {
        var table = $('#example-row-grouping-viplati').DataTable({
            "columnDefs": [
                {"visible": false, "targets": 2}
            ],
            "order": [[2, 'asc']],
            "displayLength": 100,
            "drawCallback": function (settings) {
                var api = this.api();
                var rows = api.rows({page: 'current'}).nodes();
                var last = null;

                api.column(2, {page: 'current'}).data().each(function (group, i) {
                    if (last !== group) {
                        $(rows).eq(i).before(
                            '<tr class="group info"><td colspan="4" class="text-dark text-center" style="vertical-align: middle">' + group + '</td></tr>'
                        );

                        last = group;
                    }
                });
            }
        });

        // Order by the grouping
        $('#example-row-grouping-viplati tbody').on('click', 'tr.group', function () {
            var currentOrder = table.order()[0];
            if (currentOrder[0] === 2 && currentOrder[1] === 'asc') {
                table.order([2, 'desc']).draw();
            } else {
                table.order([2, 'asc']).draw();
            }
            return false;
        });
    }

    if ($('#example-edit').length) {
        $('#example-edit').DataTable();
        $('#example-edit').editableTableWidget();
    }
})(jQuery);