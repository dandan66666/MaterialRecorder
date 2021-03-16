[TOC]

## API

### 添加记录

```
url: record/add
method: post
post_data(json):
	name: string
	number: integer
	record_time: timestamp
	specifications: string
	price: float
	construction: string
```

### 获得所有记录（记录列表）

```
url: record/list
method: post
post_data(json):
	page_num: integer
	page_size: integer
	- name: string
	- number: integer
	- price: float
	- specifications: string
	- start_time: integer
	- end_time: integer
	- construction: string
return(json):
	{
	error_code: integer
	error_msg: string
	records: [{id: integer
                name: string
                number: integer
                record_time: timestamp
                specifications: string
                price: float,
                construction: string}, {...}, {...}，... ]
     total_price: integer
     total_number: integer
     total_records: integer
     }
备注： post_data中以“-”开头的为list的限制条件，可选可不选，不加限制就不写该限制条件。specifications可以只写规格中的关键词。start_time和end_time为1970-1-1至记录时间的微秒数。
```

### 获得记录详情

```
url: record/detail/<id>
method: get
return(json):
{
	records: [
	{id: integer
	name: string
	number: integer
	record_time: integer
	specifications: string
	price: float
	construction: string}
	],
	total_number: integer,
	total_price: integer,
	total_records: integer
}
```

### 删除记录

```
url: record/delete/<id>
method: delete
```

### 修改记录

```
url: record/modify
method: post
post_data(json):
	id: integer
	name: string
	number: integer
	record_time: timestamp
	specifications: string
	price: float
	construction: string
```

### 获取工地列表

```
url: construction/list
method: get
return(json):
{
    error_code: integer
    error_msg: string
    constructions: [string, string, ...]
}
```



## 错误码

```
Success=0
RecordNotExist= -1
SearchTypeNotExist=-2
ChangeNameForbidden=-3
ServerInternalError=-4
MultiRecords=-5
WrongInput=-6
GetConstructionError=-7
```

