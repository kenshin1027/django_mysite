function addbook(bookid,url){
	$.ajax({
	type:'GET',
	url:url,
	data:{
		'bookid':bookid,
	},
	dataType:'json',
	success:function(json)
	{
		var result=json.result;
		if (result==0)
		{
			if (url.match('cart'))
			{
				$('#poptips').text('ok,已经将本书放进您的借书车');
			}
			else
			{
				$('#poptips').text('ok,已经将本书收藏');
			}
			$('#myModal').modal('show');
		}
		else if (result==1)
		{
			if (url.match('cart'))
			{
				$('#poptips').text('该书已经在您的借书车中了喔');	
			}
			else{
				$('#poptips').text('该书已经在您的收藏中了喔');	
			}
			
			$('#myModal').modal('show');
		}
		else
			$('#loginmodal').modal('show');				
	}
});
}


function filterbooklist(filter){
	console.log('in filter_booklist now')
	$.ajax({
		type: 'GET',
		url:"/mylibrary/filter_booklist",
		data:{
			"filter": JSON.stringify(filter),
		},
		dataType: 'json',
		success: function(json) 
		{
			console.log('response in')
			var result = json.result;
			if (result == 0) 
			{
				var bookitems =JSON.parse(json.bookitems);
				var maxindex =JSON.parse(json.maxindex);
				totalpages=JSON.parse(json.totalpages);
  				showbooklist(bookitems);
  				if (filter.pageindex==1)  //代表是重新筛选，所以刷新pageindex
  					showpageindex(maxindex,totalpages)
			}
			else
			{
				$('#firstpage').children('div').css({'display':'none'});
				$('#firstpage').html('没有找到符合条件的书。')
			}
		},
	});
}


function searchbooklist(searchtext){
	$.ajax({
		type:'GET',
		url:'/mylibrary/search_booklist',
		data:{
			'searchtext':searchtext,	
		},
		dataType:'json',
		success:function(json)
		{
			var result=json.result;
			if (result==0)
			{
				var bookitems =JSON.parse(json.bookitems);
				var maxindex =JSON.parse(json.maxindex);
				totalpages=JSON.parse(json.totalpages);	
				showbooklist(bookitems);
				showpageindex(maxindex,totalpages);
			}
			else
			{
				$('#firstpage').children('div').css({'display':'none'});
				$('#firstpage').html('没有找到符合条件的书。')
			}	

		},
	});
}