$(document).ready(function () {
  $("#tableObj").DataTable({
    ajax: "https://57d5-202-39-243-126.jp.ngrok.io/mongoapi",

    columns: [
      //列的標題一般是從DOM中讀取（也可以使用這個屬性為表格創建列標題)
      { data: "Real_name", title: "姓名" },
      { data: "Line_name", title: "Line暱稱" },
      { data: "Gender", title: "性別" },
      { data: "Age", title: "年齡" },
      { data: "Reserve_Date", title: "預約日期" },
      { data: "Reserve_Time", title: "預約時間" },
      {
        data: "Video_link",
        title: "視訊連結",
        render: function (data, type, row) {
          return (
            "<a href=" +
            data +
            ' target="_blank" class="btn btn-outline-primary" role="button" aria-pressed="true">進入視訊診間</a> '
          );
        },
      },
    ],
    language: {
      url: "https://cdn.datatables.net/plug-ins/1.11.3/i18n/zh_Hant.json",
    },
    columnDefs: [
      {
        targets: 1,
        className: "dt-body-center dt-head-center", //欄位文字置中
      },
      {
        targets: 2,
        className: "dt-body-center dt-head-center",
      },
      {
        targets: 3,
        className: "dt-body-center dt-head-center",
      },
      {
        targets: 4,
        className: "dt-body-center dt-head-center",
      },
      {
        targets: 5,
        className: "dt-body-center dt-head-center",
      },
      {
        targets: 6,
        className: "dt-body-center dt-head-center",
      },
    ],
  });
});
