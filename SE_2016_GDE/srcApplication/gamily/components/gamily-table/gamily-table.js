(function () {
    Ember.TEMPLATES['defaultItemContainer'] = Ember.Handlebars.compile("{{text}}");
    Ember.TEMPLATES['components/gamily-table'] = Ember.Handlebars.compile('' +
        '{{table-component columnsBinding="columns" contentBinding="content" hasFooter=false isSortable=true}}' +
        '');

    var GamilyTableComponent = Ember.Component.extend({
        ajaxURL: '_some_default_path_if_gets_overwrite_',
        ajaxResponse: 'will_come_from_API',
        requestSent: false,
        requestFinished: false,
        getData: Ember.A(),
        variable: "",
        selectContentInRequest: function (response) {
            path = this.get('variable');
            if(path != "") {
                path_ = path.split(".");
                for(var i=0; i<path_.length; ++i){
                    response = response[path_[i]];
                }
            }
            return response;
        },
        columns: function() {
            if(this.get('requestSent') == false) {
                this.toggleProperty('requestSent');
                this.fetchData();
            }
            if(this.get('requestFinished') == false) {
                return [];
            }
            columnsData = this.get('columns_data');
            if(columnsData === undefined) {
                return [];
            }
            return columnsData
        }.property('columns_data'),
        content: function() {
            contentData = this.get('content_data');
            if(contentData === undefined) {
                return [];
            }
            return contentData;
        }.property('content_data'),
        fetchData: function() {
            var parent = this;
            var success = function(data) {
                parent.set('ajaxResponse', data);
            };
            this.cAjax({
                type: 'GET',
                url: this.get('ajaxURL'),
                data: JSON.parse(this.get('getData')),
                success: success
            });
        }.observes('ajaxURL'),
        cAjax : function (obj) {
            return $.ajax({
                dataType: obj['dataType'] ? obj['dataType'] : "JSON",
                url: obj['url'],
                type: obj['type'] ? obj['type'] : "GET",
                data: obj['data'],
                retryCount: obj['retryCount'] ? obj['retryCount'] : 0,
                retryLimit: 10,
                success: function (data) {
                    if (typeof obj['success'] == 'function') {
                        obj['success'](data);
                    }
                },
                error: function (data) {
                    if (data.status > 498 && this.retryCount < this.retryLimit) {
                        obj['retryCount'] = obj['retryCount'] ? obj['retryCount'] + 1 : 1;
                        setTimeout(function () {
                            cAjax(obj);
                        }, 2000);
                    } else {
                        if (typeof obj['error'] == 'function') {
                            obj['error'](data);
                        }
                    }
                }

            });
        },
        processData: function() {
            response = this.get('ajaxResponse');
            //leaderBoardData = response.data.scores;
            leaderBoardData = this.selectContentInRequest(response);
            this.createColumns(leaderBoardData[0]);
            this.createContent(leaderBoardData);
            this.toggleProperty('requestFinished');
        }.observes('ajaxResponse'),
        createColumns: function(dataSingleRow) {
            var output = [];
            for(var key in dataSingleRow) {
                var col = Ember.Table.ColumnDefinition.create({
                    textAlign: 'text-align-center',
                    headerCellName: this.capitalize(key),
                    cellKey: key,
                    isSortable: true,
                    getCellContent: function(row) {
                        return row.get(this.cellKey);
                    }
                });
                output.push(col);
            }
            this.set('columns_data', output);
        },
        createContent: function(data) {
            data_dict = [];
            for(i=0; i<data.length; i++) {
                row_dict = {};
                for(key in data[i]) {
                    row_dict[key] = data[i][key];
                }
                data_dict.push(row_dict);
            }
            this.set('content_data', data_dict);
        },
        capitalize: function(string){
            return string.replace( /(^|\s)([a-z])/g , function(m,p1,p2){ return p1+p2.toUpperCase(); } );
        }
    });

    Ember.Application.initializer({
        name:"gamily-table",
        initialize:function (container, application) {
            container.register('component:gamily-table', GamilyTableComponent);
        }
    });
})();