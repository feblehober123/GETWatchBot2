/* Kabo-chan's GET Functions (http://pastebin.com/E1ZfnHvL),
 * brought to you as a C extension for Python.
 * This software is licensed under the WTFPL (http://wtfpl.org) */

/* le file not found error on GENTOO GNU/Linux so absolute path */
#include "/usr/include/python2.7/Python.h"

PyMODINIT_FUNC initrepdigits(void);

int main(int argc, char *argv[])
{
	Py_SetProgramName(argv[0]);
	Py_Initialize();
	initrepdigits();
	Py_Exit(0);
	return 0;
}

static PyObject * repdigits_test(PyObject *self, PyObject* args)
{
	int num = 0;
	if (!PyArg_ParseTuple(args, "i", &num))
	return NULL;
	printf("%d\n", num);
	//return Py_BuildValue("i", num);
	return PyInt_FromLong(42L);
}

static PyObject * repdigits_repdigits(PyObject *self, PyObject *args)
{
	int repdig	= 0;
	int pdigit	= -1;	//previous digit
	int cdigit	= 0;	//current digit
	int num;
	if (!PyArg_ParseTuple(args, "i", &num))
		return NULL;
	
	 do {
		cdigit = num % 10;
		if (cdigit != pdigit && pdigit != -1)
			return Py_BuildValue("i", repdig); //non-repeating digit located
		repdig++;
		pdigit = cdigit;
	} while (num /= 10);
	return Py_BuildValue("i", repdig);
}

/* nextget: determine the next n-digit GET based on the current post number */
static PyObject * repdigits_nextget(PyObject *self, PyObject *args)
{
	int num, n;
	if (!PyArg_ParseTuple(args, "ii", &num, &n))
		return NULL;
	int unchanged, repdigit, repdigits, i, tpow, digits[n];
	unchanged = num;
	
	/* separate unchanged digits */
	tpow = (int)pow(10,n);
	unchanged /= tpow;
	unchanged *= tpow;	//Erase n low-order digits. Possibly could be more efficient?
	
	/* generate array of digits to be changed */
	for (i=n-1; i >= 0 && num; i--) {
		digits[i] = num % 10;
		num /= 10;
	}
	
	/* run comparisons to determine the repeating digit of the next get */
	repdigit = digits[0];	//repdigit must be stored elsewhere so that
							//it can be mutated without changing the digits
	for (i=0; i < n; i++)
		if (digits[0] < digits[i]) {
			repdigit++;
			if (repdigit > 9)
				repdigit = 0;
			break;
		} else if (digits[0] > digits[i])
			break;
	if (i==n && digits[0]==digits[i-1]) {
		repdigit++;
		if (repdigit > 9)
			repdigit = 0;
	}
	/* assemble the repeating digit into a repeating integer of n columns */
	repdigits = repdigit;
	for (; n > 1; n--)
		repdigits = repdigits * 10 + repdigit;
	
	/* return the sum of the unchanged digits and the repeating digits */
	return Py_BuildValue("i", unchanged + repdigits);
}


static PyMethodDef repdigits_methods[] = {
	{"repdigits", repdigits_repdigits, METH_VARARGS,
		"returns the count of repeating digits in a number"},
	{"nextget", repdigits_nextget, METH_VARARGS,
		"determine the next n-digit GET based on the current post num"},
	{NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC initrepdigits(void)
{
	PyImport_AddModule("repdigits");
	Py_InitModule("repdigits", repdigits_methods);
}
