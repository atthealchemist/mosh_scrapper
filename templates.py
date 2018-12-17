from string import Template

course_lecture = Template("https://codewithmosh.com/courses/$course_id/lectures/$lecture_id")
course_url = Template("https://codewithmosh.com/courses/enrolled/$course_id")
wistia_json_url_template = Template("https://fast.wistia.com/embed/medias/$wistia_id.json?callback=result")
saved_directory_template = Template("Saved directory: $directory")
cookie_store_template = Template("Cookie: $cookie")
download_lecture_from_course_template = Template('Downloading "$lecture" from "$course" @ "$directory"... ')
exception_template = Template("Can't load lecture #$lecture! \nDetails:\n$exception")