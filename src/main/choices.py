# choices for skills and languages


SKILL_COMPETENCY_CHOICES = (
    ('', '-----'),
    (1, 'Below Average'),
    (2, 'Average'),
    (3, 'Good'),
    (4, 'Excellent'), )

LANGUAGE_COMPETENCY_CHOICES = (
  ('', '-----'),
    (1, "Beginner"),
    (2, "Elementary"),
    (3, "Intermediate"),
    (4, "Upper-Intermediate"),
    (5, "Advanced"),
    (6, "Native"),)



CV_CHOICES = (
    ('jakarta', 'Jakarta'),
    ('new_york', 'New York'),
    ('tokyo', 'Tokyo'),
    ('rome', 'Rome'),
    ('san_francisco', 'San Francisco'), 
    )

 
SECTION_CHOICE = (
    ('work_experience', 'Experience'), 
    ('education', 'Education'),
    ('certifications', 'Certifications'),
    ('courses', 'Courses'),
    ('projects', 'Projects'), 
    ('publications', 'Publications'), 
    ('skills', 'Skills'), 
    ('languages','Languages'),
    ('hobbies','Hobbies'),
    ('custom_section', 'Custom Section'),
    )
