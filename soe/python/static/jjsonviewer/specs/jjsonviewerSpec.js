describe("jjsonviewer jquery plugin", function() {
	var fixture = "<div id='jjson'></div>",
		json = null;	

	beforeEach(function(){
		setFixtures(fixture);
	});

	it("should parse json with number", function() {
		json = '{"number1": 12345678}';
		$("#jjson").jJsonViewer(json);		

		var key = $(".jjson-container").find(".key:eq(1)").text(),
			value = parseInt($(".jjson-container").find(".number").text());

		expect(value).toBe(12345678);
		expect(key).toContain('"number1"');	
	});

	it("should parse json with string", function() {
		json = '{"string": "name"}';
		$("#jjson").jJsonViewer(json);		

		var key = $(".jjson-container").find(".key:eq(1)").text(),
			value = $(".jjson-container").find(".string").text();

		expect(value).toBe('"name"');
		expect(key).toContain('"string"');	
	});

	it("should parse json with boolean", function() {
		json = '{"boolean": true}';
		$("#jjson").jJsonViewer(json);		

		var key = $(".jjson-container").find(".key:eq(1)").text(),
			value = !!$(".jjson-container").find(".boolean").text();

		expect(value).toBe(true);
		expect(key).toContain('"boolean"');	
	});

	it("should parse json with array", function() {
		json = '{"array": [1, true, "string"]}';
		$("#jjson").jJsonViewer(json);		

		var key = $(".jjson-container").find(".key:eq(1)").text(),
			number = parseInt($(".jjson-container").find(".array").find(".number").text()),
			booleanValue = !!$(".jjson-container").find(".array").find(".boolean").text(),
			string = $(".jjson-container").find(".array").find(".string").text();	

		expect(number).toBe(1);
		expect(booleanValue).toBe(true);
		expect(string).toBe('"string"');	
		expect(key).toContain('"array"');	
	});

	it("should hide index keys of array elements", function() {
		json = '{"array": [1, true, "string"]}';
		$("#jjson").jJsonViewer(json);		

		var keys = $(".jjson-container").find(".array .key");
		
		keys.each(function() {
			expect($(this).css("display")).toBe("none");
		});	
	});

	it("should parse json with object", function() {
		json = '{"object": {"number": 1, "string": "string"}}';
		$("#jjson").jJsonViewer(json);		

		var key = $(".jjson-container").find(".key:eq(1)").text(),
			numberKey = $(".jjson-container").find(".object:eq(1)").find(".key:eq(0)").text()
			numberValue = parseInt($(".jjson-container").find(".object:eq(1)").find(".number").text()),
			stringKey = $(".jjson-container").find(".object:eq(1)").find(".key:eq(1)").text()
			stringValue = $(".jjson-container").find(".object:eq(1)").find(".string").text();	

		expect(numberKey).toContain("number");
		expect(numberValue).toBe(1);
		expect(stringKey).toContain('"string"');
		expect(stringValue).toBe('"string"');	
		expect(key).toContain("object");	
	});

	it("should parse json with null", function() {
		json = '{"null": null}';
		$("#jjson").jJsonViewer(json);		

		var key = $(".jjson-container").find(".key:eq(1)").text(),
			value = $(".jjson-container").find(".null").text();

		expect(value).toBe('"null"');
		expect(key).toContain('"null"');	
	});
});