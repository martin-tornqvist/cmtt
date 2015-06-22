#ifndef FRAMEWORK_H
#define FRAMEWORK_H

/* A *very* minimal C unit testing "framework" */

#define CHECK(msg, test)     \
	do		     \
	{		     \
	if (!(test))	     \
	{		     \
		return msg;  \
	} while (0)

#define RUN_TEST(test)	     \
	do		     \
	{		     \
	char *msg = test();  \
	if (msg)	     \
	{		     \
		return msg;  \
	} while (0)

#endif /* FRAMEWORK_H */
